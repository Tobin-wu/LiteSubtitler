# coding: utf8
import ctypes
import os
import sys

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from config import APP_NAME, RESOURCE_PATH
from core.base_object import BaseObject
from core.image.image_tool import ImageTool
from model.file_vo import FileVO
from ui.facade.main_fcd import MainFacade

# 设置应用程序的用户模型ID，以确保任务栏图标显示正确
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)


class QrcodeBuilder(BaseObject):
    """主应用程序类，负责初始化界面、处理用户交互和任务调度。"""

    @staticmethod
    def process_qrcode(src_image_path: str, output_image_path: str, icon_png_path: str):
        # 1、截取 src_image_path 图片的二维码部分，并重设大小
        image_vo = FileVO(src_image_path)
        # 输出图像文件路径
        qrcode_image_path = image_vo.file_dir + '/' + image_vo.file_only_name + '-out.jpg'
        try:
            crop_box = (174, 576, 905, 1307)  # 二维码（周边多出一个像素， 731 * 731）
            size = (200, 200)
            ImageTool.crop_resize_image(src_image_path, qrcode_image_path, crop_box, size)

            # 2、把 icon_png_path 添加到 output_image_path 的中间
            ImageTool.overlay_image_center(qrcode_image_path, icon_png_path, output_image_path)
        finally:
            if os.path.exists(qrcode_image_path):
                os.remove(qrcode_image_path)


if __name__ == '__main__':
    QrcodeBuilder.process_qrcode(
        src_image_path="../docs/qrcode/使用群-原图.jpg",
        output_image_path="../docs/使用群.png",
        icon_png_path="../docs/wing-48.png"
    )
    QrcodeBuilder.process_qrcode(
        src_image_path="../docs/qrcode/技术群-原图.jpg",
        output_image_path="../docs/技术群.png",
        icon_png_path="../docs/pen-48.png"
    )
