# coding: utf8
import os
from enum import Enum


class TranslateModeEnum(Enum):
    """ 翻译模式 """
    FAST = '模型直译'
    PRECISE = '精细意译'
    DEEP_THOUGHT = '深思翻译'

    @classmethod
    def filter_formats(cls):
        return " ".join(f"*.{fmt.value}" for fmt in TranslateModeEnum)

    @classmethod
    def is_audio_file(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # 去掉点号并转换为小写
        return file_extension in [item.value for item in TranslateModeEnum]

    @classmethod
    def get_by_value(cls, value):
        for mode in TranslateModeEnum:
            if mode.value == value:
                return mode
        return None
