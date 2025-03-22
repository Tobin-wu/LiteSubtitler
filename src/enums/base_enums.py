# coding: utf8
from enum import Enum


class ThreeFieldEnum(Enum):
    def __new__(cls, name, code, description):
        obj = object.__new__(cls)
        obj._value_ = name  # 枚举的值，通常用于唯一标识
        obj.code = code  # 自定义字段：代码
        obj.description = description  # 自定义字段：说明
        return obj

    @staticmethod
    def find_by_code(code):
        for item in ThreeFieldEnum:
            if item.code == code:
                return item
        return None
