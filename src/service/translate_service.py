# coding: utf8
import os
from typing import Dict, Optional, Callable, Any

from config import PROMPT_PATH
from core.base_object import BaseObject
from core.llm.llm_translater import LlmTranslater
from core.asr.asr_data import ASRData
from core.srt.srt_tool import SrtTool
from settings.prompt_setting import SUMMARIZER_PROMPT, TRANSLATE_PROMPT_FAST, TRANSLATE_PROMPT_PRECISE, \
    TRANSLATE_PROMPT_DEEP_THOUGHT
from utils.dict_utils import DictUtils


class TranslateService(BaseObject):
    """
    翻译服务类，用于处理字幕的翻译任务。

    主要功能：
        1. 初始化翻译参数并执行字幕翻译。
        2. 支持批量翻译和摘要提取。
    """

    def __init__(self, log_to_ui_func: Optional[Callable] = None):
        """
        初始化翻译服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self._args = {
            "need_translate": True,  # 是否翻译
            "source_language": "英文",  # 源语言
            "target_language": "中文",  # 目标语言
            "llm_api_url": "http://127.0.0.1:11434/v1",  # LLM API 地址
            "llm_api_key": "api.key",  # LLM API 密钥
            "llm_model": "gemma2:latest",  # 使用的模型
            "need_remove_punctuation": True,  # 是否删除句子中的符号
        }

    def reset_args(self, the_args: Dict[str, Any]) -> None:
        """
        重置翻译参数。

        Args:
            the_args: 包含新参数的字典。
        """
        DictUtils.update_by_key(self._args, the_args)

    def translate_srt(self, out_file_path: str, asr_data: ASRData, batch_num: int = 10) -> ASRData:
        """
        翻译字幕文件并保存结果。

        Args:
            out_file_path: 输出文件的路径。如果为 None，则不保存文件。
            asr_data: 包含字幕数据的 ASRData 对象。
            batch_num: 每批翻译的字幕数量。

        Returns:
            翻译后的 ASRData 对象。
        """
        if not self._args['need_translate']:
            self.log_warning("无需翻译，系统配置为‘不需要翻译’")
            return asr_data

        tr_asr_data = self._inner_translate(asr_data=asr_data, batch_num=batch_num)
        if out_file_path:
            tr_asr_data.to_srt(layout='仅译文', save_path=out_file_path)
        return tr_asr_data

    def _inner_translate(self, asr_data: ASRData, batch_num: int, prev_num: int = 2) -> ASRData:
        """
        内部方法，执行字幕翻译。

        Args:
            asr_data: 包含字幕数据的 ASRData 对象。
            batch_num: 每批翻译的字幕数量。
            prev_num: 每批翻译时参考的前文数量。

        Returns:
            翻译后的 ASRData 对象。
        """
        subtitle_json = {int(k): v["original_subtitle"] for k, v in asr_data.to_json().items()}
        subtitle_length = len(subtitle_json)

        # 初始化翻译器
        translater = LlmTranslater(
            base_url=self._args["llm_api_url"],
            api_key=self._args["llm_api_key"],
            model=self._args["llm_model"],
            source_language=self._args["source_language"],
            target_language=self._args["target_language"],
            need_remove_punctuation=self._args["need_remove_punctuation"],
            subtitle_length=subtitle_length,
            log_to_ui_func=self.log_to_ui_func
        )
        # 读取提示语
        prompts = self._read_all_prompt_()

        # 提取摘要信息
        summarize_result = self._do_summarize(subtitle_content=asr_data.to_txt(),
                                              worker=translater,
                                              prompt=prompts['summarizer'])
        self.log_info(f"摘要信息：\n{summarize_result}")

        # 执行翻译
        optimizer_result = self._do_translate(
            subtitle_json=subtitle_json,
            batch_num=batch_num,
            prev_num=prev_num,
            summarize_result=summarize_result,
            translater=translater,
            prompts=prompts
        )

        # 更新翻译结果到 ASRData
        for i, subtitle_text in optimizer_result.items():
            seg = asr_data.segments[int(i) - 1]
            seg.text = subtitle_text

        return asr_data

    def _read_all_prompt_(self) -> Dict[str, str]:
        """
        读取所有的提示语。

        Returns:
            提示语对象: {
                "summarizer": summarizer_prompt,
                "FAST": translate_prompt_fast,
                "PRECISE": translate_prompt_precise,
                "DEEP_THOUGHT": translate_prompt_deep_thought
            }
        """

        def read_the_prompt(prompt_file_path: str, default_prompt: str):
            if (not os.path.exists(prompt_file_path)) or (not os.path.isfile(prompt_file_path)):
                self.log_debug(f"配置文件不存在：{prompt_file_path}")
                return default_prompt

            try:
                with open(prompt_file_path, 'r', encoding='utf-8') as file:
                    prompt = file.read()
                    return prompt
            except FileNotFoundError:
                return default_prompt

        summarizer_prompt = read_the_prompt(os.path.join(PROMPT_PATH, f"摘要.txt"),
                                            SUMMARIZER_PROMPT)
        translate_prompt_fast = read_the_prompt(os.path.join(PROMPT_PATH, f"翻译-模型直译.txt"),
                                                TRANSLATE_PROMPT_FAST)
        translate_prompt_precise = read_the_prompt(os.path.join(PROMPT_PATH, f"翻译-精细意译.txt"),
                                                   TRANSLATE_PROMPT_PRECISE)
        translate_prompt_deep_thought = read_the_prompt(os.path.join(PROMPT_PATH, f"翻译-深思翻译.txt"),
                                                        TRANSLATE_PROMPT_DEEP_THOUGHT)

        return {
            "summarizer": summarizer_prompt,
            "FAST": translate_prompt_fast,
            "PRECISE": translate_prompt_precise,
            "DEEP_THOUGHT": translate_prompt_deep_thought
        }

    def _do_translate(self, subtitle_json: Dict[int, str], batch_num: int, prev_num: int,
                      summarize_result: str, translater: LlmTranslater,
                      prompts: Dict[str, str]) -> Dict[int, str]:
        """
        执行字幕翻译任务。

        Args:
            subtitle_json: 字幕数据的字典，键为序号，值为字幕文本。
            batch_num: 每批翻译的字幕数量。
            prev_num: 每批翻译时参考的前文数量。
            summarize_result: 摘要信息。
            translater: 翻译器实例。
            prompts: 使用的提示语（多个）。

        Returns:
            翻译后的字幕字典，键为序号，值为翻译后的文本。

        Raises:
            Exception: 如果翻译过程中发生错误。
        """
        self.log_info("开始：翻译字幕")
        try:
            chunks = SrtTool.group_subtitles(subtitle_json, batch_num, prev_num)
            return translater.translate(
                original_subtitles=chunks,
                prev_num=prev_num,
                summary_content=summarize_result,
                prompts=prompts
            )
        except Exception as e:
            self.log_exception(f"翻译字幕失败: {e}")
            raise
        finally:
            self.log_info("完成：翻译字幕")

    def _do_summarize(self, subtitle_content: str, worker: LlmTranslater, prompt: str) -> str:
        """
        提取字幕摘要信息。

        Args:
            subtitle_content (str): 字幕内容。
            worker (LlmTranslater): 翻译器实例。
            prompt (str): 使用的提示语。

        Returns:
            提取的摘要信息。

        Raises:
            Exception: 如果摘要提取过程中发生错误。
        """
        self.log_info("开始：提取字幕摘要信息")
        try:
            return worker.summarize(subtitle_content=subtitle_content, prompt=prompt)
        except Exception as e:
            self.log_exception(f"字幕摘要信息提取失败: {e}")
            return ""
        finally:
            self.log_info("完成：提取字幕摘要信息")
