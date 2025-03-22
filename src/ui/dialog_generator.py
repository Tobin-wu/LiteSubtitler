# coding: utf8
import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QFileDialog, QFrame, QColorDialog, QMessageBox

from config import ConfigTool
from enums.supported_audio_enum import SupportedAudioEnum
from enums.supported_subtitle_enum import SupportedSubtitleEnum
from enums.supported_video_enum import SupportedVideoEnum
from ui.config_binder import ConfigBinder
from utils.style_utils import StyleUtils


class DialogGenerator:
    """对话框生成器，用于生成各种通用对话框（如文件选择、颜色选择等）。"""

    @staticmethod
    def open_url(parent: QWidget, url: str):
        """打开指定的URL链接。

        Args:
            parent (QWidget): 父窗口，用于显示错误对话框。
            url (str): 需要打开的URL链接。

        Raises:
            如果无法打开URL，会弹出错误提示框。
        """
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.critical(parent, '错误', f'无法打开URL: {url}\n错误: {e}')

    @staticmethod
    def select_medium_files(parent: QWidget) -> list[str]:
        """打开文件选择对话框，选择支持的媒体文件（视频、音频、字幕）。

        Args:
            parent (QWidget): 父窗口，用于显示文件选择对话框。

        Returns:
            list[str]: 用户选择的文件路径列表。
        """
        # 获取支持的视频、音频、字幕文件格式
        video_formats = SupportedVideoEnum.filter_formats()
        audio_formats = SupportedAudioEnum.filter_formats()
        subtitle_formats = SupportedSubtitleEnum.filter_formats()

        # 构建文件过滤器字符串
        filter_str = (
            f"媒体文件 ({video_formats} {audio_formats});;"
            f"视频文件 ({video_formats});;"
            f"音频文件 ({audio_formats});;"
            f"字幕文件 ({subtitle_formats})"
        )

        # 打开文件选择对话框
        file_names, _ = QFileDialog.getOpenFileNames(
            parent,
            "选择媒体文件",
            "",
            filter_str
        )
        return file_names

    @staticmethod
    def select_and_set_color(
        parent: QWidget,
        frame: QFrame,
        config_args: dict,
        key_path: list[str] = None,
        default_color: QColor = None
    ):
        """打开颜色选择对话框，设置QFrame的背景色并更新配置。

        Args:
            parent (QWidget): 父窗口，用于显示颜色选择对话框。
            frame (QFrame): 需要设置背景色的QFrame组件。
            config_args (dict): 配置字典，用于存储颜色值。
            key_path (list[str], optional): 配置字典中颜色值的路径。默认为None。
            default_color (QColor, optional): 默认颜色值。默认为None。
        """
        # 初始化颜色为白色
        init_color = Qt.GlobalColor.white

        # 从QFrame的样式表中提取背景色
        back_color = StyleUtils.background_color_in_stylesheet(frame.styleSheet())
        if back_color:
            init_color = QColor(back_color)

        # 如果提供了默认颜色且有效，则使用默认颜色
        the_color = init_color.name()
        if default_color and default_color.isValid():
            the_color = default_color.name()

        # 打开颜色选择对话框
        color = QColorDialog.getColor(
            initial=init_color,
            parent=parent,
            title="选择颜色"
        )

        # 如果用户选择了有效颜色，则更新颜色值
        if color and color.isValid():
            the_color = color.name()

        # 设置QFrame的背景色
        ConfigBinder.reset_frame_color(frame=frame, color=the_color)

        # 更新配置字典中的颜色值
        if key_path:
            ConfigTool.reset_config_attr(config_dict=config_args, key_path=key_path, the_value=the_color)
