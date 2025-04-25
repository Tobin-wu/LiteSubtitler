# coding: utf8
import json
import math
import re
from pathlib import Path
from typing import List

from .asr_data_seg import ASRDataSeg

CHARS_PER_PHONEME = 4  # 每个音素包含的字符数


class ASRData:

    def __init__(self, segments: List[ASRDataSeg]):
        """
        创建。

        Args:
            segments: ASR数据分段列表。
        """
        self.audio_file = ""
        # 去除 segments 中 text 为空的部分，并按开始时间排序
        self.segments = sorted(
            (seg for seg in segments if seg.text and seg.text.strip()),
            key=lambda x: x.start_time
        )

    def __iter__(self):
        return iter(self.segments)

    def __len__(self) -> int:
        return len(self.segments)

    def has_data(self) -> bool:
        """检查是否包含任何发声数据"""
        return bool(self.segments)

    def is_word_timestamp(self) -> bool:
        """
        判断是否是字级时间戳。
        规则：
        1. 对于英文，每个 segment 应该只包含一个单词。
        2. 对于中文，每个 segment 应该只包含一个汉字。
        3. 允许 20% 的误差率。
        """
        if not self.segments:
            return False

        valid_segments = sum(
            1 for seg in self.segments
            if (len(seg.text.strip().split()) == 1 and seg.text.isascii()) or len(seg.text.strip()) <= 4
        )
        return (valid_segments / len(self.segments)) >= 0.8

    def split_to_word_segments(self):
        """
        将当前 ASRData 中的每个 segment 按字词分割，并按音素计算时间戳，每 4 个字符视为一个音素单位进行时间分配。
        """
        new_segments = []

        for seg in self.segments:
            text = seg.text
            duration = seg.end_time - seg.start_time

            # 匹配所有有效字符（包括数字）
            pattern = (r'[a-zA-Z\']+|\d+'
                       r'|[\u4e00-\u9fff]|[\u3040-\u309f]|[\u30a0-\u30ff]|[\uac00-\ud7af]'
                       r'|[\u0e00-\u0e7f]|[\u0600-\u06ff]|[\u0400-\u04ff]|[\u0590-\u05ff]'
                       r'|[\u1e00-\u1eff]|[\u3130-\u318f]')
            words_list = list(re.finditer(pattern, text))

            if not words_list:
                continue

            # 计算总音素数
            total_phonemes = sum(math.ceil(len(w.group()) / CHARS_PER_PHONEME) for w in words_list)
            time_per_phoneme = duration / max(total_phonemes, 1)  # 防止除零

            current_time = seg.start_time
            for word_match in words_list:
                word = word_match.group()
                # 计算当前词的音素数
                word_phonemes = math.ceil(len(word) / CHARS_PER_PHONEME)
                word_duration = int(time_per_phoneme * word_phonemes)

                # 创建新的字词级 segment
                word_end_time = min(current_time + word_duration, seg.end_time)
                new_segments.append(ASRDataSeg(
                    text=word,
                    start_time=current_time,
                    end_time=word_end_time
                ))

                current_time = word_end_time

        self.segments = new_segments

    def save(self, save_path: str, ass_style: str = None, layout: str = "原文在上") -> None:
        """
        将 ASRData 保存到文件。

        Args:
            save_path: 要保存到的文件。
            ass_style: ASS的样式。
            layout: 字幕布局，可选值 ["译文在上", "原文在上", "仅原文", "仅译文"]。
        Returns:
              None
        """
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        if save_path.endswith('.srt'):
            self.to_srt(save_path=save_path, layout=layout)
        elif save_path.endswith('.txt'):
            self.to_txt(save_path=save_path, layout=layout)
        elif save_path.endswith('.json'):
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_json(), f, ensure_ascii=False)
        elif save_path.endswith('.ass'):
            self.to_ass(save_path=save_path, style_str=ass_style, layout=layout)
        else:
            raise ValueError(f"不支持的文件扩展名: {save_path}")

    def to_txt(self, save_path=None, layout: str = "原文在上") -> str:
        """
        转换为纯文本字幕格式（无时间戳）。

        Args:
            save_path: 要保存到的文件。
            layout: 字幕布局，可选值 ["译文在上", "原文在上", "仅原文", "仅译文"]。
        Returns:
              str: 纯文本字幕字符串。
        """
        return self._to_txt_file(save_path=save_path, layout=layout)

    def to_srt(self, save_path=None, layout: str = "原文在上") -> str:
        """
        转换为 SRT 字幕格式。

        Args:
            save_path: 要保存到的文件。
            layout: 字幕布局，可选值 ["译文在上", "原文在上", "仅原文", "仅译文"]。
        Returns:
              str: 纯文本字幕字符串。
        """
        return self._to_txt_file(save_path=save_path, layout=layout,
                                 fmt_line_func=lambda no, ts, msg: f"{no}\n{ts}\n{msg}\n")

    def _to_txt_file(self, save_path=None, layout: str = "原文在上", fmt_line_func=None) -> str:
        """
        转换为纯文本字幕格式。

        Args:
            save_path: 要保存到的文件。
            layout: 字幕布局，可选值 ["译文在上", "原文在上", "仅原文", "仅译文"]。
            fmt_line_func: 格式化每一行字幕的函数。
        Returns:
              str: 文本字幕字符串。
        """
        result = []
        for n, seg in enumerate(self.segments, 1):
            # 检查是否有换行符
            if "\n" in seg.transcript:
                original, translated = seg.transcript.split("\n", 1)
            else:
                original, translated = seg.transcript, ""

            # 根据字幕类型组织文本
            if layout == "原文在上":
                text = f"{original}\n{translated}" if translated else original
            elif layout == "译文在上":
                text = f"{translated}\n{original}" if translated else original
            elif layout == "仅原文":
                text = original
            elif layout == "仅译文":
                text = translated if translated else original
            else:
                text = seg.transcript

            if fmt_line_func:
                result.append(fmt_line_func(n, seg.to_srt_ts(), text))
            else:
                result.append(text)
        text = "\n".join(result)
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
        return text

    def to_lrc(self, save_path=None) -> str:
        """
        转换为 LRC 字幕格式。

        Args:
            save_path: 要保存到的文件。
        Returns:
              str: LRC字幕的字符串。
        """
        lrc_text = "\n".join(
            f"{seg.to_lrc_ts()}{seg.transcript}" for seg in self.segments
        )
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(lrc_text)
        return lrc_text

    def to_json(self) -> dict:
        """
        转换为 JSON 格式。

        Returns:
            dict: 字幕的JSON字典数据。
        """
        result_json = {}
        for i, segment in enumerate(self.segments, 1):
            # 检查是否有换行符
            if "\n" in segment.text:
                original_subtitle, translated_subtitle = segment.text.split("\n", 1)
            else:
                original_subtitle, translated_subtitle = segment.text, ""

            result_json[str(i)] = {
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "original_subtitle": original_subtitle,
                "translated_subtitle": translated_subtitle
            }
        return result_json

    def to_ass(self, style_str: str = None, layout: str = "原文在上", save_path: str = None) -> str:
        """
        转换为 ASS 字幕格式。

        Args:
            style_str(str, optional): ASS 样式字符串，为空则使用默认样式。
            layout(str, optional): 字幕布局，可选值 ["译文在上", "原文在上", "仅原文", "仅译文"]。
            save_path(str, optional): 保存的文件。
        Returns:
            str: ASS 格式字幕内容。
        """
        if not style_str:
            style_str = (
                "[V4+ Styles]\n"
                "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,"
                "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
                "Alignment,MarginL,MarginR,MarginV,Encoding\n"
                "Style: Default,MicrosoftYaHei-Bold,40,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1\n"
                "Style: Secondary,MicrosoftYaHei-Bold,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1"
            )

        ass_content = (
            "[Script Info]\n"
            "; Script generated by VideoCaptioner\n"
            "; https://github.com/weifeng2333\n"
            "ScriptType: v4.00+\n"
            "PlayResX: 1280\n"
            "PlayResY: 720\n\n"
            f"{style_str}\n\n"
            "[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        )

        dialogue_template = 'Dialogue: 0,{},{},{},,0,0,0,,{}\n'
        for seg in self.segments:
            start_time, end_time = seg.to_ass_ts()
            if "\n" in seg.text:
                original, translate = seg.text.split("\n", 1)
                if layout == "译文在上" and translate:
                    ass_content += dialogue_template.format(start_time, end_time, "Secondary", original)
                    ass_content += dialogue_template.format(start_time, end_time, "Default", translate)
                elif layout == "原文在上" and translate:
                    ass_content += dialogue_template.format(start_time, end_time, "Secondary", translate)
                    ass_content += dialogue_template.format(start_time, end_time, "Default", original)
                elif layout == "仅原文":
                    ass_content += dialogue_template.format(start_time, end_time, "Default", original)
                elif layout == "仅译文" and translate:
                    ass_content += dialogue_template.format(start_time, end_time, "Default", translate)
            else:
                ass_content += dialogue_template.format(start_time, end_time, "Default", seg.text)

        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(ass_content)
        return ass_content

    @staticmethod
    def read_ass_style(style_args) -> str:
        """
        读取 ASS 字幕样式。

        Args:
            style_args: 配置参数。
        Returns:
              str: ASS字幕样式字符串。
        """
        style_format = ("Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,"
                        "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
                        "Alignment,MarginL,MarginR,MarginV,Encoding")
        return (f"[V4+ Styles]\n{style_format}\n"
                f"{ASRData.read_ass_font_style(style_args['default_style'])}\n"
                f"{ASRData.read_ass_font_style(style_args['secondary_style'])}")

    @staticmethod
    def read_ass_font_style(font_args):
        """
        读取 ASS 字体样式。

        Args:
            font_args: 字体配置参数。
        Returns:
              str: ASS字体样式字符串。
        """
        def read_color(val: str):
            return val.strip().replace("#", "&H00").upper()

        return (f"Style: {font_args['Name']},{font_args['Fontname']},{font_args['Fontsize']},"
                f"{read_color(font_args['PrimaryColour'])},"
                f"{read_color(font_args['SecondaryColour'])},"
                f"{read_color(font_args['OutlineColour'])},"
                f"{read_color(font_args['BackColour'])},"
                f"{font_args['Bold']},{font_args['Italic']},{font_args['Underline']},{font_args['StrikeOut']},"
                f"{font_args['ScaleX']},{font_args['ScaleY']},{font_args['Spacing']},{font_args['Angle']},"
                f"{font_args['BorderStyle']},{font_args['Outline']},{font_args['Shadow']},{font_args['Alignment']},"
                f"{font_args['MarginL']},{font_args['MarginR']},{font_args['MarginV']},{font_args['Encoding']}")

    def merge_segments(self, start_index: int, end_index: int, merged_text: str = None):
        """
        合并从 start_index 到 end_index 的段（包含），处理结果直接放在self.segments中。

        Args:
            start_index: 开始位置索引值
            end_index: 结束位置索引值
            merged_text: 合并处理的文本。
        Returns:
              None
        """
        if start_index < 0 or end_index >= len(self.segments) or start_index > end_index:
            raise IndexError("无效的段索引")
        merged_start_time = self.segments[start_index].start_time
        merged_end_time = self.segments[end_index].end_time
        if merged_text is None:
            merged_text = ''.join(seg.text for seg in self.segments[start_index:end_index + 1])
        merged_seg = ASRDataSeg(merged_text, merged_start_time, merged_end_time)
        # 替换 segments[start_index:end_index+1] 为 merged_seg
        self.segments[start_index:end_index + 1] = [merged_seg]

    def merge_with_next_segment(self, index: int) -> None:
        """
        合并指定索引的段与下一个段。

        Args:
            index: 当前索引值。
        """
        if index < 0 or index >= len(self.segments) - 1:
            raise IndexError("索引超出范围或没有下一个段可合并")
        current_seg = self.segments[index]
        next_seg = self.segments[index + 1]
        merged_text = f"{current_seg.text} {next_seg.text}"
        merged_seg = ASRDataSeg(merged_text, current_seg.start_time, next_seg.end_time)
        self.segments[index] = merged_seg
        # 删除下一个段
        del self.segments[index + 1]

    def remove_or_add_space_for_segments(self):
        """将当前 ASRData 中的每个 segment 中的两个空格修改为一个空格"""
        for seg in self.segments:
            text = seg.text.strip()

            # 定义需要检查的符号列表
            symbols = [".", ",", "!", "?", ":", ";", "。", "，", "！", "？", "：", "；"]

            # 构建正则表达式模式，匹配符号后面没有空格的情况
            pattern = rf'([{"".join(symbols)}])(?!\s)'

            # 使用 re.sub() 函数进行替换，在符号后面添加一个空格
            text = re.sub(pattern, r'\1 ', text)

            # 连续大于等于 2 个空格时替换为一个空格
            seg.text = re.sub(r' {2,}', ' ', text)

    def __str__(self):
        return self.to_txt()
