from enum import Enum


class ImagePosEnum(Enum):
    LEFT_TOP = "左上角"
    RIGHT_TOP = "右上角"
    LEFT_BOTTOM = "左下角"
    RIGHT_BOTTOM = "右下角"

    @classmethod
    def read_by_text(cls, text: str):
        for item in ImagePosEnum:
            if item.value == text:
                return item
        return None