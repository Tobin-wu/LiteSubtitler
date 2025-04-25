# coding: utf8
from enums.image_pos_enum import ImagePosEnum


class ImageEmbedArg:

    def __init__(self,
                 file_path: str,
                 scale: str = '100:-1',
                 color_channel_mixer: float = 0.6,
                 overlay_width: str = 'W-w-20',
                 overlay_height: str = 'H-h-20',
                 enable_time_period: str = 'between(t, 0, 29)'):
        """
        初始化 ImageEmbedArg 实例。

        Args:
            file_path(str): 文件路径
            scale(str): 图片分辨率
            color_channel_mixer(str): 透明度
            overlay_width(str): 覆盖宽
            overlay_height(str): 覆盖高
            enable_time_period(str): 有效时间段
        """
        self.file_path = file_path
        self.scale = scale
        self.color_channel_mixer = color_channel_mixer

        self.overlay_width = overlay_width
        self.overlay_height = overlay_height
        self.enable_time_period = enable_time_period

    @staticmethod
    def read_pos_overlay(pos: ImagePosEnum, offset_width: int, offset_height: int):
        if pos == ImagePosEnum.LEFT_TOP:
            return f'{offset_width}:{offset_height}'
        elif pos == ImagePosEnum.RIGHT_TOP:
            return f'W-w-{offset_width}:{offset_height}'
        elif pos == ImagePosEnum.LEFT_BOTTOM:
            return f'{offset_width}:H-h-{offset_height}'
        elif pos == ImagePosEnum.RIGHT_BOTTOM:
            return f'W-w-{offset_width}:H-h-{offset_height}'
        else:
            return f'{offset_width}:{offset_height}'
