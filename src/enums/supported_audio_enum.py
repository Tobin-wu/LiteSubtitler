# coding: utf8
import os
from enum import Enum


class SupportedAudioEnum(Enum):
    """ 支持的音频格式 """
    AAC = "aac"
    AC3 = "ac3"
    AIFF = "aiff"
    AMR = "amr"
    APE = "ape"
    AU = "au"
    FLAC = "flac"
    M4A = "m4a"
    MP2 = "mp2"
    MP3 = "mp3"
    MKA = "mka"
    OGA = "oga"
    OGG = "ogg"
    OPUS = "opus"
    RA = "ra"
    WAV = "wav"
    WMA = "wma"

    @classmethod
    def filter_formats(cls):
        return " ".join(f"*.{fmt.value}" for fmt in SupportedAudioEnum)

    @classmethod
    def is_audio_file(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # 去掉点号并转换为小写
        return file_extension in [item.value for item in SupportedAudioEnum]
