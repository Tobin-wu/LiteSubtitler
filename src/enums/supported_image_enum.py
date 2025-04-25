# coding: utf8
import os
from enum import Enum


class SupportedImageEnum(Enum):
    """ 支持的图片格式 """
    BMP = "bmp"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

    @classmethod
    def filter_formats(cls):
        return " ".join(f"*.{fmt.value}" for fmt in SupportedImageEnum)

    @classmethod
    def is_image_file(cls, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # 去掉点号并转换为小写
        return file_extension in [item.value for item in SupportedImageEnum]
