# coding: utf8
import os
import subprocess
import sys

from config import ICON_REC
from model.unique_key_value_map import UniqueKeyValueMap
from ui.data.array_table_model import ArrayTableModel
from ui.driver.gui_tool import GuiTool
from ui.gui.main_frm import Ui_frmMain


class MainFrmHelper:
    """主窗口辅助类，提供日志记录、图标加载、模型加载等功能。"""

    @staticmethod
    def fill_icon(ui: Ui_frmMain):
        """为UI中的按钮设置图标。

        Args:
            ui (Ui_frmMain): 主窗口的UI对象。
        """
        # 设置按钮图标
        icon = GuiTool.build_icon(ICON_REC.get('add'))
        ui.btnAddFile.setIcon(icon)
        ui.actAddFile.setIcon(icon)

        icon = GuiTool.build_icon(ICON_REC.get('clear'))
        ui.btnClearFile.setIcon(icon)
        ui.actClearFile.setIcon(icon)

        ui.btnStart.setIcon(GuiTool.build_icon(ICON_REC.get('run')))
        ui.btnStop.setIcon(GuiTool.build_icon(ICON_REC.get('stop')))

        ui.actLlmChecker.setIcon(GuiTool.build_icon(ICON_REC.get('llm_check_tool')))
        ui.actImageEmbed.setIcon(GuiTool.build_icon(ICON_REC.get('png')))
        ui.actSubtitleEmbed.setIcon(GuiTool.build_icon(ICON_REC.get('srt')))

        ui.actExit.setIcon(GuiTool.build_icon(ICON_REC.get('exit')))
        ui.actGitee.setIcon(GuiTool.build_icon(ICON_REC.get('gitee')))
        ui.actGithub.setIcon(GuiTool.build_icon(ICON_REC.get('github')))
        ui.actFeiShu.setIcon(GuiTool.build_icon(ICON_REC.get('feishu')))
        ui.actAbout.setIcon(GuiTool.build_icon(ICON_REC.get('about')))

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
    def ui_and_args_map(ui: Ui_frmMain) -> UniqueKeyValueMap:
        """创建UI组件与配置键的映射关系。

        Args:
            ui (Ui_frmMain): 主界面的UI对象。

        Returns:
            UniqueKeyValueMap: UI组件与配置键的映射关系。
        """
        ui_map = UniqueKeyValueMap()

        # 翻译相关参数映射
        ui_map.add(("translate_args", "need_translate"), ui.ckbTranslate.objectName())
        ui_map.add(("translate_args", "need_remove_punctuation"), ui.ckbClearPunctuation.objectName())
        ui_map.add(("translate_args", "translate_mode"), ui.cbbTranslateMode.objectName())
        ui_map.add(("translate_args", "source_language"), ui.cbbSourceLanguage.objectName())
        ui_map.add(("translate_args", "target_language"), ui.cbbTargetLanguage.objectName())

        # 字幕相关参数映射
        ui_map.add(("subtitle_args", "is_embed_subtitle"), ui.ckbEmbedSubtitle.objectName())
        ui_map.add(("subtitle_args", "subtitle_layout"), ui.cbbSubtitleLayout.objectName())

        return ui_map
