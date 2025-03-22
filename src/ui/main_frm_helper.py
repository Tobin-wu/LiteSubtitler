# coding: utf8
import logging
import os
import subprocess
import sys
from datetime import datetime

from core.llm.opanai_checker import OpenAiChecker
from ui.array_table_model import ArrayTableModel
from ui.main_frm import Ui_frmMain
from config import ICON_REC

from PyQt6.QtWidgets import QComboBox, QTextEdit, QTableView, QHeaderView
from PyQt6.QtGui import QIcon, QTextCursor, QPixmap


class MainFrmHelper:
    """主窗口辅助类，提供日志记录、图标加载、模型加载等功能。"""

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
    def fill_icon(ui: Ui_frmMain):
        """为UI中的按钮设置图标。

        Args:
            ui (Ui_frmMain): 主窗口的UI对象。
        """
        # 设置按钮图标
        ui.btnAddFile.setIcon(MainFrmHelper.build_icon(ICON_REC.get('add')))
        ui.btnClearFile.setIcon(MainFrmHelper.build_icon(ICON_REC.get('clear')))
        ui.btnStart.setIcon(MainFrmHelper.build_icon(ICON_REC.get('run')))
        ui.btnStop.setIcon(MainFrmHelper.build_icon(ICON_REC.get('stop')))
        ui.btnSetting.setIcon(MainFrmHelper.build_icon(ICON_REC.get('save-setting')))
        ui.btnSettingVisible.setIcon(MainFrmHelper.build_icon(ICON_REC.get('setting-hide')))

        ui.btnDownTool.setIcon(MainFrmHelper.build_icon(ICON_REC.get('download')))
        ui.btnDownModel.setIcon(MainFrmHelper.build_icon(ICON_REC.get('download-model')))
        ui.btnLlmApi.setIcon(MainFrmHelper.build_icon(ICON_REC.get('register-llm')))
        ui.btnLlmRefresh.setIcon(MainFrmHelper.build_icon(ICON_REC.get('refresh')))
        ui.btnWhisperExe.setIcon(MainFrmHelper.build_icon(ICON_REC.get('file')))
        ui.btnWhisperDir.setIcon(MainFrmHelper.build_icon(ICON_REC.get('dir')))
        ui.btnCheckApi.setIcon(MainFrmHelper.build_icon(ICON_REC.get('link')))

        # 设置颜色选择按钮的图标
        icon = MainFrmHelper.build_icon(ICON_REC.get('color'))
        ui.btnMainColor.setIcon(icon)
        ui.btnMainOutlineColor.setIcon(icon)
        ui.btnSecondColor.setIcon(icon)
        ui.btnSecondOutlineColor.setIcon(icon)

    @staticmethod
    def load_llm_models(cbb_llm_model: QComboBox, base_url: str, api_key: str,
                        current_model: str, config_args) -> int:
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
        if (base_url == 'https://api.siliconflow.cn/v1' and
                api_key == 'sk-wlyrgyaimjzndvavtogmqssbjdajdvdkzpqbeiyrqaoeivno'):
            models = ['THUDM/glm-4-9b-chat', 'Qwen/Qwen2.5-7B-Instruct', 'THUDM/chatglm3-6b']
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
    def is_ffmpeg_installed() -> bool:
        """检查系统中是否安装了FFmpeg。

        Returns:
            bool: 如果FFmpeg已安装返回True，否则返回False。
        """
        if sys.platform == 'win32':
            # 在Windows上使用subprocess.run检查FFmpeg
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            return result.returncode == 0
        else:
            # 在非Windows系统上使用os.system检查FFmpeg
            return os.system("ffmpeg -version") == 0

    @staticmethod
    def build_model_tasks(model: ArrayTableModel) -> list[dict]:
        """从ArrayTableModel中构建任务列表。

        Args:
            model (ArrayTableModel): 包含任务数据的表格模型。

        Returns:
            list[dict]: 任务列表，每个任务是一个字典。
        """
        tasks = []
        row_count = model.rowCount()
        col_count = model.columnCount()

        if row_count > 0:
            for row in range(row_count):
                # 获取当前行的所有数据
                items = [model.index(row, column).data() for column in range(col_count)]
                if items[1] != '*':
                    task = {
                        "id": items[0],
                        "fileName": items[1],
                        "progressRatio": items[2],
                        "progressDesc": items[3],
                        "filePath": items[4]
                    }
                    tasks.append(task)
        return tasks

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
