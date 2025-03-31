# coding: utf8
from enum import Enum

from enums.base_enums import ThreeFieldEnum


class SubtitleLanguageEnum(Enum):
    CHINESE_SIMPLIFIED = "简体中文(Chinese, Simplified)"
    CHINESE_TRADITIONAL = "繁体中文(Chinese, Traditional)"
    ENGLISH_US = "美式英语(American English)"
    ENGLISH_UK = "英式英语(British English)"
    JAPANESE = "日语(Japanese)"
    KOREAN = "韩语(Korean)"
    RUSSIAN = "俄语(Russian)"
    GERMAN = "德语(German)"
    FRENCH = "法语(French)"
    ITALIAN = "意大利语(Italian)"
    SPANISH = "西班牙语(Spanish)"
    TURKISH = "土耳其语(Turkish)"
    ARABIC = "阿拉伯语(Arabic)"
    PORTUGUESE = "葡萄牙语(Portuguese)"
    AFRIKAANS = "南非荷兰语(Afrikaans)"
    AMHARIC = "阿姆哈拉语(Amharic)"
    ASSAMESE = "阿萨姆语(Assamese)"
    AZERBAIJANI = "阿塞拜疆语(Azerbaijani)"
    BULGARIAN = "保加利亚语(Bulgarian)"
    BANGLA = "孟加拉语(Bangla)"
    BENGALI = "印度西孟加拉语(Bengali)"
    BOSNIAN = "波斯尼亚语(Bosnian)"
    CATALAN = "加泰罗尼亚语  (Catalan)"
    CZECH = "捷克语(Czech)"
    WELSH = "威尔士语(Welsh)"
    DANISH = "丹麦语(Danish)"
    GREEK = "希腊语(Greek)"
    ESTONIAN = "爱沙尼亚语(Estonian)"
    BASQUE = "巴斯克语  (Basque)"
    PERSIAN = "波斯语(Persian)"
    FINNISH = "芬兰语(Finnish)"
    FILIPINO = "菲律宾语(Filipino)"
    IRISH = "爱尔兰语(Irish)"
    GALICIAN = "加利西亚语  (Galician)"
    GUJARATI = "古吉拉特语(Gujarati)"
    HEBREW = "希伯来语(Hebrew)"
    HINDI = "印地语(Hindi)"
    CROATIAN = "克罗地亚语(Croatian)"
    HUNGARIAN = "匈牙利语(Hungarian)"
    ARMENIAN = "亚美尼亚语(Armenian)"
    INDONESIAN = "印尼语(Indonesian)"
    ICELANDIC = "冰岛语(Icelandic)"
    INUKTITUT = "因纽特语(Inuktitut)"
    JAVANESE = "爪哇语(Javanese)"
    GEORGIAN = "格鲁吉亚语(Georgian)"
    KAZAKH = "哈萨克语(Kazakh)"
    KHMER = "高棉语(Khmer)"
    KANNADA = "卡纳达语(Kannada)"
    LAO = "老挝语(Lao)"
    LITHUANIAN = "立陶宛语(Lithuanian)"
    LATVIAN = "拉脱维亚语(Latvian)"
    MACEDONIAN = "马其顿语(Macedonian)"
    MALAYALAM = "马拉雅拉姆语(Malayalam)"
    MONGOLIAN = "蒙古语(Mongolian)"
    MARATHI = "马拉地语(Marathi)"
    MALAY = "马来语(Malay)"
    MALTESE = "马耳他语(Maltese)"
    BURMESE = "缅甸语(Burmese)"
    NORWEGIAN = "挪威书面语(Norwegian Bokmål)"
    NEPALI = "尼泊尔语(Nepali)"
    DUTCH = "荷兰语(Dutch)"
    ODIA = "奥里亚语(Odia)"
    PUNJABI = "旁遮普语(Punjabi)"
    POLISH = "波兰语(Polish)"
    PASHTO = "普什图语(Pashto)"
    ROMANIAN = "罗马尼亚语(Romanian)"
    SINHALA = "僧伽罗语(Sinhala)"
    SLOVAK = "斯洛伐克语(Slovak)"
    SLOVENIAN = "斯洛文尼亚语(Slovenian)"
    SOMALI = "索马里语(Somali)"
    ALBANIAN = "阿尔巴尼亚语(Albanian)"
    SERBIAN = "塞尔维亚语(Serbian)"
    SUNDANESE = "巽他语(Sundanese)"
    SWEDISH = "瑞典语(Swedish)"
    KISWAHILI = "斯瓦希里语(Kiswahili)"
    TAMIL = "泰米尔语(Tamil)"
    TELUGU = "泰卢固语(Telugu)"
    THAI = "泰语(Thai)"
    UKRAINIAN = "乌克兰语(Ukrainian)"
    URDU = "乌尔都语(Urdu)"
    UZBEK = "乌兹别克语(Uzbek)"
    VIETNAMESE = "越南语(Vietnamese)"
    ISIZULU = "祖鲁语(isiZulu)"


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
