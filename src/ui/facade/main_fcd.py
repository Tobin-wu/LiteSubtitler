# coding: utf8
import logging
import os
from pathlib import Path
from typing import Optional

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QComboBox, QWidget,
    QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QFontComboBox, QPushButton
)

from config import ConfigTool, GITEE_REPO_URL, GITHUB_REPO_URL, FEISHU_DOWNLOAD_URL
from controller.subtitles_controller import MainController
from core.llm.opanai_checker import OpenAiChecker
from enums.language_enums import AudioLanguageEnum, SubtitleLanguageEnum
from enums.supported_subtitle_enum import SubtitleLayoutEnum
from enums.translate_mode_enum import TranslateModeEnum
from ui.base_config_facade import BaseConfigFacade
from ui.data.array_table_model import ArrayTableModel
from ui.driver.gui_tool import GuiTool
from ui.facade.about_fcd import AboutFacade
from ui.facade.image_embed_fcd import ImageEmbedFacade
from ui.facade.llm_prompter_fcd import LlmPrompterFacade
from ui.facade.main_frm_helper import MainFrmHelper
from ui.facade.setting_fcd import SettingFacade
from ui.facade.subtitle_embed_fcd import SubtitleEmbedFacade
from ui.gui.main_frm import Ui_frmMain
from utils.path_utils import PathUtils
from utils.uuid_utils import UuidUtils

# 运行状态常量
RUN_STATUS_INIT = 0  # 初始状态
RUN_STATUS_DOING = 1  # 运行中
RUN_STATUS_PAUSE = 2  # 暂停


class MainFacade(BaseConfigFacade):
    """主应用程序外观类，负责初始化界面、处理用户交互和任务调度。"""

    def __init__(self):
        """初始化实例。"""
        super().__init__(log_to_ui_func=self.write_log, config=ConfigTool.read_config_setting())

        self.llm_ok = False  # LLM连接状态

        # 初始化主窗口
        self.mainWindow = QMainWindow()
        self.ui = Ui_frmMain()
        self.ui.setupUi(self.mainWindow)
        self.mainWindow.showMaximized()  # 最大化

        # 初始化组件映射和界面
        self.uiArgsMap = MainFrmHelper.ui_and_args_map(self.ui)
        self._init_form_()

        # 初始化运行状态和任务模型
        self.run_status = RUN_STATUS_INIT
        self.model = self._build_table_view_model()

        # 初始化任务控制器
        self.controller = MainController(
            model=self.model,
            finished_all_callback=self._on_all_task_finished,
            config_args=self.config_args,
            log_to_ui_func=self.write_log
        )

    def show_main_form(self) -> None:
        """显示主窗口。"""
        self.mainWindow.show()

    def set_app_icon(self, app_icon: QIcon) -> None:
        """设置应用的图标。

        Args:
            app_icon (QIcon): 应用程序的图标
        """
        if app_icon:
            self.mainWindow.setWindowIcon(app_icon)

    def write_log(self, msg: str, logger_name: Optional[str] = None, level: int = logging.INFO) -> None:
        """记录日志到UI界面。

        Args:
            msg (str): 日志消息
            logger_name (Optional[str]): 日志名称，默认为类名
            level (int): 日志级别，默认为INFO
        """
        logger_name = logger_name or self.__class__.__name__
        if self.config_args["LOG_SETTING"]["level"] <= level:
            GuiTool.write_log(
                msg=msg,
                logger_name=logger_name,
                level=level,
                txt_log=self.ui.txtLog
            )

    def _init_form_(self) -> None:
        """初始化窗口。"""
        # 日志框样式设置
        self.ui.txtLog.setStyleSheet("QTextEdit { background-color: #2B2B2B; color: #A9B7C6; border: 1px solid gray; }")

        # 组件初始化和数据绑定
        self._init_form_comp_()
        self._fill_args_to_ui()

    def _fill_args_to_ui(self) -> None:
        """将配置参数填充到UI组件。"""
        GuiTool.fill_widget(
            widgets=self.ui.freSetting.findChildren(QWidget),
            config_args=self.config_args,
            ui_map=self.uiArgsMap
        )

    def _init_form_comp_(self) -> None:
        """初始化窗口上的组件。"""
        MainFrmHelper.fill_icon(self.ui)

        # 按钮事件绑定
        buttons = [
            (self.ui.btnAddFile, self._on_add_file_),
            (self.ui.btnClearFile, self._on_clear_all_file),
            (self.ui.btnStart, self._on_start_run),
            (self.ui.btnStop, self._on_stop_run),
        ]
        for btn, handler in buttons:
            btn.clicked.connect(handler)

        self.ui.actClearFile.triggered.connect(self._on_clear_all_file)
        self.ui.actAddFile.triggered.connect(self._on_add_file_)
        self.ui.actSetting.triggered.connect(self._on_open_setting_dlg_)
        self.ui.actExit.triggered.connect(self.mainWindow.close)

        self.ui.actLlmChecker.triggered.connect(self._on_open_prompt_dlg_)
        self.ui.actSubtitleEmbed.triggered.connect(self._on_open_srt_embed_dlg_)
        self.ui.actImageEmbed.triggered.connect(self._on_open_image_embed_dlg_)

        self.ui.actGitee.triggered.connect(lambda: self._on_open_url_(GITEE_REPO_URL))
        self.ui.actGithub.triggered.connect(lambda: self._on_open_url_(GITHUB_REPO_URL))
        self.ui.actFeiShu.triggered.connect(lambda: self._on_open_url_(FEISHU_DOWNLOAD_URL))
        self.ui.actAbout.triggered.connect(self._on_open_about_dlg_)

        enable_languages = self._read_enable_languages_()

        # 初始化下拉框
        combobox_configs = [
            (self.ui.cbbSourceLanguage, AudioLanguageEnum, None, None,
             lambda item: self._config_set_audio_language(item)),
            (self.ui.cbbTargetLanguage, SubtitleLanguageEnum, ["translate_args", "target_language"],
             SubtitleLanguageEnum.CHINESE_SIMPLIFIED.value, None,
             lambda val: val if val in enable_languages else None),
            (self.ui.cbbTranslateMode, TranslateModeEnum, ["translate_args", "translate_mode"],
             TranslateModeEnum.PRECISE.value),
            (self.ui.cbbSubtitleLayout, SubtitleLayoutEnum, ["subtitle_args", "subtitle_layout"],
             SubtitleLayoutEnum.TRANSLATE_ON_TOP.value)
        ]
        for config in combobox_configs:
            self._init_combobox_(*config)

    def _on_open_setting_dlg_(self):
        """配置"""
        try:
            fcd_setting = SettingFacade(func_write_log=self.write_log,
                                        config=self.config_args)
            fcd_setting.show()
        finally:
            self._fill_args_to_ui()

    def _on_open_srt_embed_dlg_(self):
        """字幕合成工具"""
        fcd_srt_embed = SubtitleEmbedFacade(func_write_log=self.write_log,
                                            config=self.config_args,
                                            use_cuda=self.controller.use_cuda,
                                            icon=self.ui.actSubtitleEmbed.icon())
        fcd_srt_embed.show()

    def _on_open_image_embed_dlg_(self):
        """图片嵌入工具"""
        fcd_image_embed = ImageEmbedFacade(func_write_log=self.write_log,
                                           config=self.config_args,
                                           use_cuda=self.controller.use_cuda,
                                           icon=self.ui.actImageEmbed.icon())
        fcd_image_embed.show()

    def _on_open_about_dlg_(self):
        """关于"""
        fcd_about = AboutFacade(func_write_log=self.write_log)
        fcd_about.show()

    def _on_open_prompt_dlg_(self):
        """提示语调整工具"""
        fcd_llm_tool = LlmPrompterFacade(
            func_write_log=self.write_log,
            config={
                "base_url": self.config_args['translate_args']['llm_api_url'],
                "api_key": self.config_args['translate_args']['llm_api_key'],
                "models": [],
                "PROMPT_FILES": self.config_args["PROMPT_FILES"]
            },
            icon=self.ui.actLlmChecker.icon()
        )
        fcd_llm_tool.show()

    def _on_open_url_(self, url) -> None:
        """打开指定的URL。"""
        GuiTool.open_url(parent=self.mainWindow, url=url)

    def _read_enable_languages_(self):
        if "SHOW_LANGUAGES" in self.config_args:
            if "enabled" in self.config_args["SHOW_LANGUAGES"]:
                if self.config_args["SHOW_LANGUAGES"]["enabled"]:
                    if "languages" in self.config_args["SHOW_LANGUAGES"]:
                        return self.config_args["SHOW_LANGUAGES"]["languages"]
        return [member.value for member in SubtitleLanguageEnum]

    def _write_all_config(self) -> None:
        """将UI配置写入配置文件。"""
        GuiTool.widget_to_config(
            widgets=self.ui.freSetting.findChildren(QWidget),
            config_args=self.config_args,
            ui_map=self.uiArgsMap
        )
        # 特殊值的处理
        self.config_args['subtitle_args']['default_style']['MarginV'] = self.config_args['subtitle_args'][
            'subtitle_margin_v']
        self.config_args['subtitle_args']['secondary_style']['MarginV'] = self.config_args['subtitle_args'][
            'subtitle_margin_v']

        ConfigTool.save_config_setting(self.config_args)

    def _config_set_audio_language(self, item: AudioLanguageEnum) -> None:
        """设置音频语言配置。

        Args:
            item (AudioLanguageEnum): 音频语言枚举值。
        """
        if isinstance(item, AudioLanguageEnum):
            self.config_args['asr_args']['language'] = item.code
            self.config_args['translate_args']['source_language'] = item.value

    def _ui_obj_enabled(self, enabled: bool) -> None:
        """
        设置UI控件的启用状态。

        Args:
            enabled (bool): 是否启用控件。
        """
        self.ui.btnStart.setEnabled(enabled)
        self.ui.btnAddFile.setEnabled(enabled)
        self.ui.btnClearFile.setEnabled(enabled)

        # 遍历所有子控件并设置启用状态
        GuiTool.set_ui_enabled(self.ui.freSetting.findChildren(QWidget), enabled)

    def _on_start_run(self) -> None:
        """开始运行任务前的准备工作。"""
        faster_whisper_dir = os.path.dirname(self.config_args['asr_args']['faster_whisper_path'])
        PathUtils.append_to_env_path(faster_whisper_dir)

        # 检查工具和模型是否准备就绪
        if self._check_tool():
            self._write_all_config()  # 将配置信息写入self.config
            self._do_start_tasks()
        else:
            self.log_warning("运行需要的工具和模型不完整！！！")

    def _check_tool(self) -> bool:
        """
        检查运行所需的工具和模型是否准备就绪。

        Returns:
            bool: 如果所有工具和模型都准备就绪，返回True；否则返回False。
        """
        # 检查FFmpeg是否安装
        if not MainFrmHelper.is_ffmpeg_installed():
            self.log_warning("FFmpeg没有安装。")
            return False
        self.log_info("FFmpeg 准备就绪!")

        # 检查FasterWhisper是否安装
        whisper_exe = self.config_args['asr_args']['faster_whisper_path']
        if not os.path.exists(whisper_exe):
            self.log_warning("Faster Whisper 没有安装。")
            return False
        self.log_info("FasterWhisper 准备就绪!")

        # 检查FasterWhisper模型是否安装
        whisper_dir = self.config_args['asr_args']['model_dir']
        whisper_model = os.path.join(whisper_dir, f"faster-whisper-{self.config_args['asr_args']['whisper_model']}")

        if not os.path.exists(whisper_dir) or not os.path.exists(whisper_model):
            self.log_warning(f"Faster Whisper 模型没有安装: {whisper_model}")
            return True  # 会自动下载
        self.log_info("FasterWhisper模型 准备就绪!")

        # 检查LLM配置是否有效
        if not self.llm_ok:
            is_success, message = OpenAiChecker.test_openai(base_url=self.config_args['translate_args']['llm_api_url'],
                                                            api_key=self.config_args['translate_args']['llm_api_key'],
                                                            model=self.config_args['translate_args']['llm_model'])
            if not is_success:
                self.log_warning(f"LLM配置有问题：{message}")
                return False
        self.log_info("LLM 准备就绪!")

        return True

    def _do_start_tasks(self) -> None:
        """开始执行任务。"""
        tasks = MainFrmHelper.build_model_tasks(self.model)
        if tasks:
            self.run_status = RUN_STATUS_DOING
            self._ui_obj_enabled(False)
            self._process_tasks(tasks)
        else:
            self.log_warning("请先选择要处理的视频文件。")

    def _process_tasks(self, tasks) -> None:
        """处理任务列表。

        Args:
            tasks: 要处理的任务列表。
        """
        self.controller.run(tasks=tasks, args=self.config_args)

    def _on_all_task_finished(self) -> None:
        """所有任务完成后的处理。"""
        self._ui_obj_enabled(True)
        self.run_status = RUN_STATUS_INIT

    def _on_stop_run(self) -> None:
        """停止运行任务。"""
        if self.run_status == RUN_STATUS_DOING:
            self.controller.stop()
        self._ui_obj_enabled(True)
        self.run_status = RUN_STATUS_INIT

    def _on_clear_all_file(self) -> None:
        """清除所有文件。"""
        if self.run_status == RUN_STATUS_INIT:
            self.model.clear()

    def _on_add_file_(self) -> None:
        """显示选择文件对话框并添加文件。"""
        file_names = GuiTool.select_medium_files(self.mainWindow)
        if file_names:
            for file_name in file_names:
                self.model.append_row([UuidUtils.generate_guid(), Path(file_name).name, '0', '待处理', file_name])

    def _build_table_view_model(self) -> ArrayTableModel:
        """构建表格视图模型。

        Returns:
            ArrayTableModel: 构建好的表格视图模型。
        """
        data = [
            ['0', '*', '0', '', '']
        ]
        headers = ['id', '名称', '进度', '步骤', '路径']
        sizes = [250, 200, 60, 200]
        return GuiTool.build_tv_model(tv=self.ui.tbvTask,
                                      data=data,
                                      headers=headers,
                                      sizes=sizes)
