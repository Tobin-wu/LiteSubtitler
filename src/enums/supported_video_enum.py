# coding: utf8
import os
from enum import Enum


class SupportedVideoEnum(Enum):
    """ 支持的视频格式 """
    MP4 = "mp4"
    WEBM = "webm"
    OGM = "ogm"
    MOV = "mov"
    MKV = "mkv"
    AVI = "avi"
    WMV = "wmv"
    FLV = "flv"
    M4V = "m4v"
    TS = "ts"
    MPG = "mpg"
    MPEG = "mpeg"
    VOB = "vob"
    ASF = "asf"
    RM = "rm"
    RMVB = "rmvb"
    M2TS = "m2ts"
    MTS = "mts"
    DV = "dv"
    GXF = "gxf"
    TOD = "tod"
    MXF = "mxf"
    F4V = "f4v"

    @classmethod
    def filter_formats(cls):
        return " ".join(f"*.{fmt.value}" for fmt in SupportedVideoEnum)

    @classmethod
    def is_video_file(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # 去掉点号并转换为小写
        return file_extension in [item.value for item in SupportedVideoEnum]
