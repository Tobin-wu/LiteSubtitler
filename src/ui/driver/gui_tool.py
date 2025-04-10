# coding: utf8
import logging
import os
import webbrowser
from datetime import datetime
from typing import Optional, Callable, Dict

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QTextCursor, QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QFileDialog, QFrame, QColorDialog, QMessageBox, QLineEdit, QCheckBox, QSpinBox, \
    QDoubleSpinBox, QFontComboBox, QComboBox, QTextEdit, QTableView, QHeaderView

from config import ConfigTool, SILICON_API_KEY, SILICON_MODELS, SILICON_API_URL
from core.llm.opanai_checker import OpenAiChecker
from enums.supported_audio_enum import SupportedAudioEnum
from enums.supported_subtitle_enum import SupportedSubtitleEnum
from enums.supported_video_enum import SupportedVideoEnum
from model.unique_key_value_map import UniqueKeyValueMap
from ui.data.array_table_model import ArrayTableModel
from utils.style_utils import StyleUtils


class GuiTool:
    """界面处理工具，用于生成各种通用对话框，通用操作等。"""

    @staticmethod
    def open_and_select_file(parent: QWidget, caption: str, filter_str: str, file_edit: QLineEdit) -> str:
        file, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=caption,
            filter=filter_str
        )
        if file and file_edit:
            file_edit.setText(file)
        return file

    @staticmethod
    def load_llm_models(cbb_llm_model: QComboBox, base_url: str, api_key: str,
                        current_model: str, config_args=None) -> int:
        """加载LLM模型列表到QComboBox中。

        Args:
            cbb_llm_model (QComboBox): 用于显示模型的下拉框。
            base_url (str): LLM API的基础URL。
            api_key (str): LLM API的密钥。
            current_model (str): 当前选中的模型。
            config_args (dict): 配置字典。

        Returns:
            int: 加载的模型数量。
        """
        # 如果是特定API和密钥，加载预定义模型
        if base_url == SILICON_API_URL and api_key == SILICON_API_KEY:
            models = SILICON_MODELS
        else:
            models = OpenAiChecker.get_openai_models(base_url=base_url, api_key=api_key)

        model_list = []
        if config_args and 'SHOW_MODELS' in config_args and config_args["SHOW_MODELS"]["enabled"] and \
                config_args["SHOW_MODELS"]["models"]:
            # 用配置中的定义模型来过滤models
            for model in config_args["SHOW_MODELS"]["models"]:
                if model in models:
                    model_list.append(model)
        if len(model_list) == 0:
            model_list = models

        # 如果有模型，加载到下拉框中
        if model_list and len(model_list) > 0:
            cbb_llm_model.clear()
            cbb_llm_model.view().setSpacing(2)
            cbb_llm_model.addItems(model_list)
            if current_model in model_list:
                cbb_llm_model.setCurrentText(current_model)
            else:
                cbb_llm_model.setCurrentText(model_list[0])
            return len(model_list)
        return 0

    @staticmethod
    def init_combobox(combobox: QComboBox,
                      values: Dict[str, str],
                      on_combobox_changed: Optional[Callable] = None,
                      filter_for_items: Optional[Callable] = None) -> None:
        """
        初始化QComboBox，填充枚举值并连接信号槽。

        Args:
            combobox (QComboBox): 要初始化的QComboBox实例。
            values (Dict[str, str]): 用于填充QComboBox的选项。
            on_combobox_changed (Optional[Callable]): 下拉列表变化时的处理器。
            filter_for_items (Optional[Callable]): 下拉列表项目的过滤器。
        """
        # 设置QComboBox的下拉列表项之间的间隔
        combobox.clear()
        combobox.view().setSpacing(2)

        # 填充QComboBox
        if filter_for_items:
            for name, value in values.items():
                if filter_for_items(name):
                    combobox.addItem(name, value)
        else:
            for name, value in values.items():
                combobox.addItem(name, value)

        # 连接信号和槽，当用户选择一个选项时触发
        if on_combobox_changed:
            combobox.currentIndexChanged.connect(on_combobox_changed)

    @staticmethod
    def build_tv_model(tv: QTableView, data: list[list[str]], headers: list[str], sizes: list[int]) -> ArrayTableModel:
        """构建并设置QTableView的模型。

        Args:
            tv (QTableView): 需要设置模型的表格视图。
            data (list[list[str]]): 表格数据。
            headers (list[str]): 表头。
            sizes (list[int]): 每列的宽度。

        Returns:
            ArrayTableModel: 构建的表格模型。
        """
        model = ArrayTableModel(data, headers)
        tv.setModel(model)

        # 设置表头样式
        horizontal_header = tv.horizontalHeader()
        for i, size in enumerate(sizes):
            if i == len(headers) - 1:
                horizontal_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                horizontal_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                horizontal_header.resizeSection(i, size if size else 200)

        if len(headers) > len(sizes):
            for i in range(len(sizes), len(headers)):
                horizontal_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # 设置表头字体和样式
        font = horizontal_header.font()
        font.setBold(True)
        horizontal_header.setFont(font)
        horizontal_header.setStyleSheet("""
            QHeaderView::section {
                background-color: lightgray;
                color: black;
                font-weight: bold;
                padding: 4px;
                border: 1px solid gray;
            }
        """)

        # 设置垂直表头样式
        vertical_header = tv.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        vertical_header.setDefaultSectionSize(40)
        vertical_header.setStyleSheet("""
            QHeaderView::section {
                background-color: lightblue;
                color: black;
                font-weight: bold;
                padding: 4px;
                border: 1px solid gray;
            }
        """)

        return model

    @staticmethod
    def build_icon(icon_path: str) -> QIcon | None:
        """根据图标路径构建QIcon对象。

        Args:
            icon_path (str): 图标文件的路径。

        Returns:
            QIcon: 构建的QIcon对象，如果路径无效则返回None。
        """
        if os.path.exists(icon_path) and os.path.isfile(icon_path):
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path), QIcon.Mode.Normal, QIcon.State.Off)
            return icon
        return None

    @staticmethod
    def write_log(msg: str, logger_name: str, level: int, txt_log: QTextEdit):
        """将日志信息写入QTextEdit组件中。

        Args:
            msg (str): 日志消息内容。
            logger_name (str): 日志记录器的名称。
            level (int): 日志级别（如logging.INFO, logging.ERROR等）。
            txt_log (QTextEdit): 用于显示日志的QTextEdit组件。
        """
        # 获取当前时间，精确到毫秒
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        log_level = logging.getLevelName(level)

        # 构建日志输出信息
        log_msg = f"{log_time} - {logger_name} - {log_level} - {msg}"

        # 如果日志行数超过10000行，清空日志
        if txt_log.document().lineCount() > 10000:
            txt_log.clear()

        # 将日志信息插入到QTextEdit的末尾
        cursor = txt_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(log_msg + '\n')
        txt_log.setTextCursor(cursor)

    @staticmethod
    def widget_to_config(widgets: list[QWidget], config_args, ui_map: UniqueKeyValueMap):
        """将UI组件的值同步到配置字典中。

        Args:
            widgets (list[QWidget]): 需要同步的UI组件列表。
            config_args (dict): 配置字典，用于存储UI组件的值。
            ui_map (UniqueKeyValueMap): UI组件与配置键的映射关系。
        """
        for widget in widgets:
            key_path = ui_map.get_key_from_value(widget.objectName())
            if key_path:
                if isinstance(widget, QLineEdit):
                    ConfigTool.reset_config_attr(config_dict=config_args,
                                                 key_path=key_path,
                                                 the_value=widget.text())
                elif isinstance(widget, QCheckBox):
                    ConfigTool.reset_config_attr(config_dict=config_args,
                                                 key_path=key_path,
                                                 the_value=widget.isChecked())
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    ConfigTool.reset_config_attr(config_dict=config_args,
                                                 key_path=key_path,
                                                 the_value=widget.value())
                elif isinstance(widget, QFontComboBox):
                    ConfigTool.reset_config_attr(config_dict=config_args,
                                                 key_path=key_path,
                                                 the_value=widget.currentText())

    @staticmethod
    def fill_widget(widgets: list[QWidget], config_args, ui_map: UniqueKeyValueMap):
        """用配置字典中的值填充UI组件。

        Args:
            widgets (list[QWidget]): 需要填充的UI组件列表。
            config_args (dict): 配置字典，包含UI组件的值。
            ui_map (UniqueKeyValueMap): UI组件与配置键的映射关系。
        """
        for widget in widgets:
            key_path = ui_map.get_key_from_value(widget.objectName())
            if key_path:
                value = ConfigTool.read_config_attr(config_dict=config_args, key_path=key_path)
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                elif isinstance(widget, (QComboBox, QFontComboBox)):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, QFrame):
                    GuiTool.reset_frame_color(frame=widget, color=str(value))

    @staticmethod
    def reset_frame_color(frame: QFrame, color: str):
        """重置QFrame的背景颜色。

        Args:
            frame (QFrame): 需要设置颜色的QFrame组件。
            color (str): 颜色值，可以是颜色名称或十六进制颜色代码。
        """
        frame.setStyleSheet(f"background-color: {color}; border: 1px solid black")

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
    def select_file_dialog(parent: QWidget, filter_str: str) -> str:
        """打开文件选择对话框，选择支持的媒体文件（视频、音频、字幕）。

        Args:
            parent (QWidget): 父窗口，用于显示文件选择对话框。
            filter_str (str): 文件过滤器字符串.

        Returns:
            str: 用户选择的文件路径。
        """
        if filter_str is None:
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
        file_name = QFileDialog.getOpenFileName(
            parent,
            "选择媒体文件",
            "",
            filter_str
        )
        return file_name

    @staticmethod
    def save_dialog(parent: QWidget, default_path: str, filter_str: str) -> str:
        """保存文件对话框。

        Args:
            parent (QWidget): 父窗口，用于显示文件选择对话框。
            default_path (str): 默认路径.
            filter_str (str): 文件过滤器字符串.

        Returns:
            str: 用户选择的文件路径。
        """
        if filter_str is None:
            filter_str = "Text Files (*.txt);;All Files (*)"

        # 设置默认保存路径和文件名
        dialog = QFileDialog()
        dialog.setWindowTitle("另存为")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)  # 设置为保存模式

        # 显示对话框并获取结果
        file_path, _ = dialog.getSaveFileName(
            parent=parent,
            caption="选择保存位置",
            directory=default_path,
            filter=filter_str,
            initialFilter="",
            options=QFileDialog.Option.DontConfirmOverwrite  # 不确认覆盖
        )
        return file_path

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
        GuiTool.reset_frame_color(frame=frame, color=the_color)

        # 更新配置字典中的颜色值
        if key_path:
            ConfigTool.reset_config_attr(config_dict=config_args, key_path=key_path, the_value=the_color)

    @staticmethod
    def load_image_from_url(url):
        """从URL加载图片并转换为QPixmap"""
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            return QPixmap.fromImage(QImage.fromData(response.content))
        except Exception as e:
            print(f"加载图片失败: {e}")
            return None
