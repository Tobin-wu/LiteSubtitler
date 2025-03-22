# coding: utf8
from enum import Enum

from enums.base_enums import ThreeFieldEnum


class SubtitleLanguageEnum(Enum):
    CHINESE_SIMPLIFIED = "简体中文"
    CHINESE_TRADITIONAL = "繁体中文"
    ENGLISH = "英语"
    JAPANESE = "日本文"
    KOREAN = "韩文"
    FRENCH = "法文"
    GERMAN = "德文"
    SPANISH = "西班牙文"
    ITALIAN = "意大利文"
    PORTUGUESE = "葡萄牙文"
    RUSSIAN = "俄罗斯文"
    TURKISH = "土耳其文"


class AudioLanguageEnum(ThreeFieldEnum):
    AUTO = ("自动", "auto", "AUTO")
    ENGLISH = ("英语", "en", "English")
    CHINESE = ("中文", "zh", "Chinese")
    JAPANESE = ("日本语", "ja", "Japanese")
    KOREAN = ("韩语", "ko", "Korean")
    YUE = ("粤语", "yue", "Yue")
    FRENCH = ("法语", "fr", "French")
    GERMAN = ("德语", "de", "German")
    SPANISH = ("西班牙语", "es", "Spanish")
    RUSSIAN = ("俄罗斯语", "ru", "Russian")
    PORTUGUESE = ("葡萄牙语", "pt", "Portuguese")
    TURKISH = ("土耳其语", "tr", "Turkish")
    ITALIAN = ("意大利语", "it", "Italian")

    # 为了使枚举的成员名（如 ITEM_ONE）直接返回名称字段，而不是元组
    def __str__(self):
        return self._value_

    @property
    def display_info(self):
        return f"Name: {self._value_}, Code: {self.code}, Description: {self.description}"

    @staticmethod
    def read_code(value: str):
        for item in AudioLanguageEnum:
            if item._value_ == value:
                return item.code
        return None

    @staticmethod
    def is_cjk_only(value: str) -> bool:
        return value == (AudioLanguageEnum.CHINESE._value_
                         or AudioLanguageEnum.JAPANESE._value_
                         or AudioLanguageEnum.KOREAN._value_)
