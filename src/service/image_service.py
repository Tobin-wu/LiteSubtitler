# coding: utf8
from typing import Optional

from core.base_object import BaseObject
from core.image.image_tool import ImageTool


class ImageService(BaseObject):
    """
    图片服务类，用于处理图片文件。
    """

    def __init__(self, log_to_ui_func: Optional[callable] = None):
        """
        初始化服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)

    def generate_contact_image(self,
                               out_image_path: str,
                               logo_path: str,
                               title_text: str,
                               qr_code_path: str,
                               out_image_size: tuple[int, ...] = (1280, 720),
                               bk_color: tuple[int, ...] = (255, 255, 255),
                               logo_size: tuple[int, ...] = (200, 70),
                               font_path: str = None,
                               font_size: int = 24,
                               spacing: int = 20,
                               title_color: tuple[int, ...] = (0, 0, 0),  # black, red=(255, 0, 0)
                               qr_code_size: tuple[int, ...] = (300, 300)) -> str:
        """
        生成联系的图片，从上到下，分别是：logo、title、qr_code。

        Args:
            out_image_path(str): 输出图片路径
            out_image_size(tuple[int, ...]): 输出图片尺寸
            bk_color(tuple[int, ...]): 背景颜色，RGB格式
            logo_path(str): logo图片
            logo_size(tuple[int, ...]): Logo尺寸
            title_text(str): 标题
            font_path(str): 字体文件
            font_size(int): 字号
            spacing(int): 标题和图片之间的间距
            title_color(tuple[int, ...]): 标题字体颜色，RGB格式
            qr_code_path(str): 二维码图片
            qr_code_size(tuple[int, ...]): 二维码尺寸

        Returns:
            生成的图片文件路径。
        """
        self.log_info("正在生成联系方式的图片...")
        ImageTool.generate_qr_code_image(
            output_file=out_image_path,
            title_text=title_text,
            qr_code_path=qr_code_path,
            logo_path=logo_path,
            image_size=out_image_size,
            font_path=font_path,
            font_size=font_size,
            spacing=spacing,
            qr_code_size=qr_code_size,
            logo_size=logo_size,
            title_color=title_color,
            bk_color=bk_color
        )
        self.log_info("完成生成联系方式的图片！")
        return out_image_path

