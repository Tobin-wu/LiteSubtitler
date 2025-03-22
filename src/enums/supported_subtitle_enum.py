# coding: utf8
import os
from enum import Enum


class SupportedSubtitleEnum(Enum):
    """ 支持的字幕格式 """
    SRT = "srt"
    ASS = "ass"
    JSON = "json"
    TXT = "txt"

    @classmethod
    def filter_formats(cls):
        return " ".join(f"*.{fmt.value}" for fmt in SupportedSubtitleEnum)

    @classmethod
    def is_subtitle_file(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # 去掉点号并转换为小写
        return file_extension in [item.value for item in SupportedSubtitleEnum]


class SubtitleLayoutEnum(Enum):
    """ 字幕布局 """
    TRANSLATE_ON_TOP = "译文在上"
    ORIGINAL_ON_TOP = "原文在上"
    ONLY_ORIGINAL = "仅原文"
    ONLY_TRANSLATE = "仅译文"
