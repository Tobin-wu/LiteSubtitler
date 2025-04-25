# coding: utf8
import copy
import difflib
import re
from typing import Dict, Callable, List

import retry
from openai import OpenAI

from core.base_object import BaseObject
from core.srt.srt_aligner import SrtAligner
from core.srt.srt_tool import SrtTool
from enums.language_enums import AudioLanguageEnum
from enums.translate_mode_enum import TranslateModeEnum
from settings.prompt_setting import (
    SUMMARIZER_PROMPT, TRANSLATE_PROMPT
)
from utils import json_repair

# 定义常量，限制字符串最大长度
STR_MAX_LEN = 3000


class LlmTranslater(BaseObject):
    """LLM翻译器类，用于处理字幕的翻译、摘要生成和优化。"""

    def __init__(self,
                 base_url='http://127.0.0.1:11434/v1',
                 api_key='key',
                 model: str = 'gemma2:latest',
                 source_language: str = '',
                 target_language: str = '中文',
                 need_remove_punctuation: bool = True,
                 subtitle_length: int = 0,
                 log_to_ui_func=None):
        """
        初始化LlmTranslater类。

        Args:
            base_url (str): LLM API的基础URL。
            api_key (str): LLM API的密钥。
            model (str): 使用的模型名称。
            source_language (str): 源语言。
            target_language (str): 目标语言。
            need_remove_punctuation (bool): 是否需要删除句子中的标点符号。
            subtitle_length (int): 字幕长度。
            log_to_ui_func (Callable): 用于记录日志的函数。
        """
        if not base_url or not api_key:
            raise ValueError("LLM的参数必须设置")

        super().__init__(log_to_ui_func=log_to_ui_func)

        # 判断源语言是否为中日韩文
        self.cjk_only: bool = AudioLanguageEnum.is_cjk_only(source_language)
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key)

        self.summary_content = ""
        self.target_language = target_language
        self.need_remove_punctuation = need_remove_punctuation
        self.subtitle_length = subtitle_length

    def summarize(self, subtitle_content: str, prompt: str) -> str:
        """
        生成字幕内容的摘要。

        Args:
            subtitle_content (str): 字幕内容。
            prompt (str): 使用的提示语。

        Returns:
            str: 生成的摘要内容。
        """
        the_prompt = prompt if prompt else SUMMARIZER_PROMPT

        # 限制字幕内容长度
        subtitle_content = subtitle_content[:STR_MAX_LEN]
        response = self.client.chat.completions.create(
            model=self.model,
            stream=False,
            messages=[
                {"role": "system", "content": the_prompt},
                {"role": "user", "content": f"要提取摘要的视频内容:\n{subtitle_content}"}
            ]
        )
        return str(json_repair.loads(response.choices[0].message.content))

    def translate(self,
                  original_subtitles: List[Dict[int, str]],
                  summary_content: str,
                  prompts: Dict[str, str],
                  mode: TranslateModeEnum = TranslateModeEnum.PRECISE,
                  prev_num: int = 2) -> Dict[int, str]:
        """
        翻译给定的字幕。

        Args:
            original_subtitles (List[Dict[int, str]]): 原始字幕列表。
            summary_content (str): 摘要内容。
            prompts (Dict[str, str]): 使用的提示语(多个，按翻译模式区分)。
            mode (TranslateModeEnum): 翻译模式。
            prev_num (int): 前几条字幕的数量。

        Returns:
            Dict[int, str]: 翻译后的字幕。
        """
        self.summary_content = summary_content

        if mode == TranslateModeEnum.DEEP_THOUGHT:
            return self.do_translate(original_subtitles=original_subtitles,
                                     translate_func=self._deep_translate,
                                     prompts=prompts,
                                     mode=mode,
                                     prev_num=prev_num)
        else:
            return self.do_translate(original_subtitles=original_subtitles,
                                     translate_func=self._normal_translate,
                                     prompts=prompts,
                                     mode=mode,
                                     prev_num=prev_num)

    def do_translate(self,
                     original_subtitles: List[Dict[int, str]],
                     translate_func: Callable[[Dict[int, str], TranslateModeEnum, str], Dict[int, str]],
                     prompts: Dict[str, str],
                     mode: TranslateModeEnum = TranslateModeEnum.PRECISE,
                     prev_num: int = 2) -> Dict[int, str]:
        """
        执行翻译操作。

        Args:
            original_subtitles (List[Dict[int, str]]): 原始字幕列表。
            translate_func (Callable): 翻译函数。
            prompts (Dict[str, str]): 使用的提示语(多个，按翻译模式区分)。
            mode (TranslateModeEnum): 翻译模式。
            prev_num (int): 前几条字幕的数量。

        Returns:
            Dict[int, str]: 翻译后的字幕。
        """
        doing_subtitles = copy.deepcopy(original_subtitles)
        ret = {}
        the_prompt = prompts[mode.name] if prompts[mode.name] else TRANSLATE_PROMPT
        for i in range(40):  # 最多进行40次重试
            if doing_subtitles:
                temp_re_do = []  # 临时列表，用于收集需要重新处理的字幕
                for subtitle in doing_subtitles:
                    try:
                        t_subs = translate_func(subtitle, mode, the_prompt)
                        for key, value in t_subs.items():
                            if key not in ret:
                                ret[key] = value
                    except Exception as e:
                        self.log_warning(f"有没处理好的字幕，将会重试: {e}")
                        if i == 0:  # 第一轮处理失败的，拆分为更少的行数来处理
                            temp_re_do.extend(SrtTool.group_subtitles(subtitle, 4, prev_num))
                        else:  # 第二轮之后的，不必再拆分
                            temp_re_do.append(subtitle)

                doing_subtitles = temp_re_do  # 更新需要重新处理的字幕列表
            else:
                break  # 没有需要处理的，退出重试

        # 重试40次后仍未处理好的字幕，保留原字幕
        if doing_subtitles:
            for subtitle in doing_subtitles:
                t_subs = self.build_translated_ret(subtitle, subtitle)
                for key, value in t_subs.items():
                    if key not in ret:
                        ret[key] = value

        return ret

    @retry.retry(tries=2)
    def _deep_translate(self, original_sub: Dict[int, str], mode: TranslateModeEnum, prompt_fmt: str) -> Dict[int, str]:
        """
        反思翻译字幕。

        Args:
            original_sub (Dict[int, str]): 原始字幕。
            mode (TranslateModeEnum): 翻译模式。
            prompt_fmt (str): 使用的提示语。

        Returns:
            Dict[int, str]: 翻译后的字幕。
        """
        self.log_info(
            f"[+]正在{mode.value}字幕({self.subtitle_length})：{next(iter(original_sub))} - {next(reversed(original_sub))}")
        message = self._create_translate_message(original_sub, prompt_fmt)
        response = self.client.chat.completions.create(
            model=self.model,
            stream=False,
            messages=message,
            temperature=0.7)
        response_content = json_repair.loads(response.choices[0].message.content)
        optimized_text = {int(k): v["optimized_subtitle"] for k, v in response_content.items()}
        aligned_subtitle = self.repair_subtitle(original_sub, optimized_text)
        translations = {item["optimized_subtitle"]: item["revised_translation"] for item in response_content.values()}

        translated_subtitle = {}
        for k, v in aligned_subtitle.items():
            original_text = self.remove_punctuation(v)
            translated_text = self.remove_punctuation(translations.get(v, ' '))
            translated_subtitle[k] = f"{original_text}\n{translated_text}"

        return translated_subtitle

    @retry.retry(tries=2)
    def _normal_translate(self, original_sub: Dict[int, str], mode: TranslateModeEnum, prompt_fmt: str) -> Dict[int, str]:
        """
        正常翻译字幕。

        Args:
            original_sub (Dict[int, str]): 原始字幕。
            mode (TranslateModeEnum): 翻译模式。
            prompt_fmt (str): 使用的提示语。

        Returns:
            Dict[int, str]: 翻译后的字幕。
        """
        self.log_info(
            f"[+]正在{mode.value}字幕({self.subtitle_length})：{next(iter(original_sub))} - {next(reversed(original_sub))}")

        prompt = prompt_fmt.replace("[TargetLanguage]", self.target_language)
        message = [{"role": "system", "content": prompt},
                   {"role": "user",
                    "content": f"请把如下字幕翻译为 {self.target_language}:\n```\n{str(original_sub)}\n```"}]
        response = self.client.chat.completions.create(
            model=self.model,
            stream=False,
            messages=message,
            temperature=0.7)
        response_content = json_repair.loads(response.choices[0].message.content)
        if not isinstance(response_content, dict) or len(response_content) != len(original_sub):
            if isinstance(response_content, dict):
                self.log_warning(f"翻译不正确：\n{str(self.build_translated_ret(original_sub, response_content))}")
            raise RuntimeError(f"翻译结果错误, 返回类型不正确，或者翻译后的字幕条数不正确")
        return self.build_translated_ret(original_sub, response_content)

    def build_translated_ret(self, original_sub: Dict[int, str], response_content: Dict[int, str]) -> Dict[int, str]:
        """
        构建翻译后的返回结果。

        Args:
            original_sub (Dict[int, str]): 原始字幕。
            response_content (Dict[int, str]): 翻译后的内容。

        Returns:
            Dict[int, str]: 翻译后的字幕。
        """
        translated_subtitle = {}
        original_list = list(original_sub.values())
        translated_list = list(response_content.values())
        for i, key in enumerate(original_sub.keys()):
            original_text = self.remove_punctuation(original_list[i])

            if i < len(translated_list):
                translated_text = self.remove_punctuation(translated_list[i])
            else:
                translated_text = ''

            translated_subtitle[key] = f"{original_text}\n{translated_text}"
        return translated_subtitle

    def remove_punctuation(self, text: str) -> str:
        """
        移除字幕中的标点符号。

        Args:
            text (str): 原始文本。

        Returns:
            str: 移除标点符号后的文本。
        """
        if not self.need_remove_punctuation or (self.cjk_only and not self.is_mainly_cjk(text)):
            return text

        punctuation = r'[,.!?;:，。！？；：、]'
        return re.sub(f'{punctuation}+$', '', text.strip())

    @staticmethod
    def is_mainly_cjk(text_val: str) -> bool:
        """
        判断文本是否主要由中日韩文字组成。

        Args:
            text_val (str): 文本内容。

        Returns:
            bool: 是否主要由中日韩文字组成。
        """
        cjk_patterns = [
            r'[\u4e00-\u9fff]',  # 中日韩统一表意文字
            r'[\u3040-\u309f]',  # 平假名
            r'[\u30a0-\u30ff]',  # 片假名
            r'[\uac00-\ud7af]',  # 韩文音节
        ]
        cjk_count = 0
        for pattern in cjk_patterns:
            cjk_count += len(re.findall(pattern, text_val))
        total_chars = len(''.join(text_val.split()))
        return cjk_count / total_chars > 0.4 if total_chars > 0 else False

    def _create_translate_message(self, original_sub: Dict[int, str], prompt_fmt: str) -> List[Dict[str, str]]:
        """
        创建翻译请求的消息。

        Args:
            original_sub (Dict[int, str]): 原始字幕。
            prompt_fmt (str): 使用的提示语。

        Returns:
            List[Dict[str, str]]: 翻译请求的消息。
        """
        input_content = (f"校正原始字幕并翻译为{self.target_language}:\n"
                         f"<input_subtitle>{str(original_sub)}</input_subtitle>")
        if self.summary_content:
            input_content += (f"\n以下是与字幕相关的参考资料，将基于这些资料对字幕进行校正、优化和翻译:\n"
                              f"<prompt>{self.summary_content}</prompt>\n")
        prompt = prompt_fmt.replace("[TargetLanguage]", self.target_language)
        message = [{"role": "system", "content": prompt},
                   {"role": "user", "content": input_content}]
        return message

    def repair_subtitle(self, dict1: Dict[int, str], dict2: Dict[int, str]) -> Dict[int, str]:
        """
        修复字幕对齐问题。

        Args:
            dict1 (Dict[int, str]): 原始字幕。
            dict2 (Dict[int, str]): 优化后的字幕。

        Returns:
            Dict[int, str]: 修复后的字幕。
        """
        list1 = list(dict1.values())
        list2 = list(dict2.values())
        text_aligner = SrtAligner()
        aligned_source, aligned_target = text_aligner.align_texts(list1, list2)

        assert len(aligned_source) == len(aligned_target), "对齐后字幕长度不一致"
        similar_list = self.calculate_similarity_list(aligned_source, aligned_target)
        if similar_list.count(True) / len(similar_list) >= 0.89:
            start_id = next(iter(dict1.keys()))
            modify_dict = {int(start_id) + i: value for i, value in enumerate(aligned_target)}
            return modify_dict
        else:
            self.log_error(f"修复失败！相似度：{similar_list.count(True) / len(similar_list):.2f}")
            self.log_error(f"源字幕：{list1}")
            self.log_error(f"目标字幕：{list2}")
            raise ValueError("修复失败")

    def calculate_similarity_list(self, list1: List[str], list2: List[str], threshold: float = 0.5) -> List[bool]:
        """
        计算两个列表的相似性。

        Args:
            list1 (List[str]): 第一个列表。
            list2 (List[str]): 第二个列表。
            threshold (float): 相似性阈值。

        Returns:
            List[bool]: 相似性列表。
        """
        max_len = min(len(list1), len(list2))
        similar_list = [False] * max_len

        for i in range(max_len):
            similar_list[i] = self.is_similar(list1[i], list2[i], threshold)

        return similar_list

    @staticmethod
    def is_similar(text1: str, text2: str, threshold: float = 0.4) -> bool:
        """
        判断两个文本是否相似。

        Args:
            text1 (str): 第一个文本。
            text2 (str): 第二个文本。
            threshold (float): 相似性阈值。

        Returns:
            bool: 是否相似。
        """
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        return similarity >= threshold
