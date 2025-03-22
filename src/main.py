# coding: utf8
import logging
import os
import sys
import ctypes
from enum import Enum
from pathlib import Path
from typing import Type, Any, List, Optional, Callable

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import (
    QApplication, QDialog, QFileDialog, QComboBox, QFrame, QWidget,
    QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QFontComboBox, QPushButton
)

from config import APP_NAME, RESOURCE_PATH, ConfigTool, ICON_REC
from core.base_object import BaseObject
from core.llm.opanai_checker import OpenAiChecker
from controller.subtitles_controller import MainController
from enums.faster_whisper_enums import FasterWhisperModelEnum, FasterWhisperDeviceEnum, VadMethodEnum
from enums.language_enums import AudioLanguageEnum, SubtitleLanguageEnum
from enums.supported_subtitle_enum import SubtitleLayoutEnum
from enums.translate_mode_enum import TranslateModeEnum
from ui.array_table_model import ArrayTableModel
from ui.config_binder import ConfigBinder
from ui.dialog_generator import DialogGenerator
from ui.main_frm import Ui_frmMain
from ui.main_frm_helper import MainFrmHelper
from utils.path_utils import PathUtils
from utils.uuid_utils import UuidUtils

# 设置应用程序的用户模型ID，以确保任务栏图标显示正确
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)

# 运行状态常量
RUN_STATUS_INIT = 0  # 初始状态
RUN_STATUS_DOING = 1  # 运行中
RUN_STATUS_PAUSE = 2  # 暂停


class MainApp(BaseObject):
    """主应用程序类，负责初始化界面、处理用户交互和任务调度。"""

    def __init__(self):
        """初始化应用程序实例。"""
        super().__init__(log_to_ui_func=self.write_log)

        # 系统配置信息
        self.config_args = ConfigTool.read_config_setting()
        self.llm_ok = False  # LLM连接状态

        # 初始化Qt应用程序
        self.app = QApplication(sys.argv)
        self._load_qss_()  # 加载样式表

        # 初始化主窗口
        self.mainWindow = QDialog()
        self.ui = Ui_frmMain()
        self.ui.setupUi(self.mainWindow)

        # 初始化组件映射和界面
        self.uiArgsMap = ConfigBinder.ui_and_args_map(self.ui)
        self._init_form_()
        self._load_app_logo_()

        # 初始化运行状态和任务模型
        self.run_status = RUN_STATUS_INIT
        self.model = self.build_table_view_model()

        # 初始化任务控制器
        self.controller = MainController(
            model=self.model,
            finished_all_callback=self.on_all_task_finished,
            config_args=self.config_args,
            log_to_ui_func=self.write_log
        )

    def _load_app_logo_(self) -> None:
        """加载应用程序图标。"""
        ico_file = os.path.join(RESOURCE_PATH, "images", "icons", "logo-32.ico")
        if os.path.exists(ico_file):
            icon = QIcon(ico_file)
            self.app.setWindowIcon(icon)
            self.mainWindow.setWindowIcon(icon)
        else:
            self.log_warning(f"图标文件缺失：{ico_file}")

    def _load_qss_(self) -> None:
        """加载QSS样式文件。"""
        qss_file = os.path.join(RESOURCE_PATH, "styles", "main.qss")
        if os.path.exists(qss_file):
            file = QFile(qss_file)
            if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                self.app.setStyleSheet(QTextStream(file).readAll())
        else:
            self.log_warning(f"样式文件缺失：{qss_file}")

    def _init_form_(self) -> None:
        """初始化主窗口界面组件。"""
        # 日志框样式设置
        self.ui.txtLog.setStyleSheet("QTextEdit { background-color: #2B2B2B; color: #A9B7C6; border: 1px solid gray; }")

        # 组件初始化和数据绑定
        self._init_form_comp_()
        self._fill_args_to_ui()

        # 连接信号槽
        self.ui.edtBaseUrl.textChanged.connect(self.on_llm_changed)
        self.ui.edtAPiKey.textChanged.connect(self.on_llm_changed)

    def write_log(self, msg: str, logger_name: Optional[str] = None, level: int = logging.INFO) -> None:
        """记录日志到UI界面。

        Args:
            msg (str): 日志消息
            logger_name (Optional[str]): 日志名称，默认为类名
            level (int): 日志级别，默认为INFO
        """
        logger_name = logger_name or self.__class__.__name__
        if self.config_args["LOG_SETTING"]["level"] <= level:
            MainFrmHelper.write_log(
                msg=msg,
                logger_name=logger_name,
                level=level,
                txt_log=self.ui.txtLog
            )

    def _fill_args_to_ui(self) -> None:
        """将配置参数填充到UI组件。"""
        # 初始化LLM模型
        translate_args = self.config_args['translate_args']
        self._load_llm_models(
            base_url=translate_args['llm_api_url'],
            api_key=translate_args['llm_api_key'],
            current_model=translate_args['llm_model']
        )

        # 填充配置到UI组件
        ConfigBinder.fill_widget(
            widgets=self.ui.freSetting.findChildren(QWidget),
            config_args=self.config_args,
            ui_map=self.uiArgsMap
        )

    def _init_form_comp_(self) -> None:
        """初始化界面组件和事件绑定。"""
        MainFrmHelper.fill_icon(self.ui)

        # 按钮事件绑定
        buttons = [
            (self.ui.btnAddFile, self.on_add_file),
            (self.ui.btnClearFile, self.on_clear_all_file),
            (self.ui.btnStart, self.on_start_run),
            (self.ui.btnStop, self.on_stop_run),
            (self.ui.btnSetting, self.on_save_setting),
            (self.ui.btnSettingVisible, self.on_visible_setting),
            (self.ui.btnDownTool, self.on_download_tool),
            (self.ui.btnDownModel, self.on_download_model),
            (self.ui.btnLlmApi, self.on_register_llm),
            (self.ui.btnLlmRefresh, self.on_refresh_llm_models),
            (self.ui.btnWhisperExe, self.on_select_whisper_exe),
            (self.ui.btnWhisperDir, self.on_select_whisper_dir),
            (self.ui.btnCheckApi, self.on_check_llm_api)
        ]
        for btn, handler in buttons:
            btn.clicked.connect(handler)

        # 颜色选择按钮
        color_buttons = [
            (self.ui.btnMainColor, self.ui.freMainColor,
             ["subtitle_args", "default_style", "PrimaryColour"], QColor('#5aff65')),
            (self.ui.btnMainOutlineColor, self.ui.freMainOutlineColor,
             ["subtitle_args", "default_style", "OutlineColour"], QColor('#05070d')),
            (self.ui.btnSecondColor, self.ui.freSecondColor,
             ["subtitle_args", "secondary_style", "PrimaryColour"], QColor('#ffffff')),
            (self.ui.btnSecondOutlineColor, self.ui.freSecondOutlineColor,
             ["subtitle_args", "secondary_style", "OutlineColour"], QColor('#05070d'))
        ]
        for btn, fre, path, color in color_buttons:
            btn.clicked.connect(lambda _, f=fre, p=path, c=color: self.on_select_color(f, p, c))

        # 初始化下拉框
        combobox_configs = [
            (self.ui.cbbWhisperModel, FasterWhisperModelEnum, ["asr_args", "whisper_model"],
             FasterWhisperModelEnum.LARGE_V2.value),
            (self.ui.cbbRunDevice, FasterWhisperDeviceEnum, ["asr_args", "device"], FasterWhisperDeviceEnum.CPU.value),
            (self.ui.cbbVadMethod, VadMethodEnum, ["asr_args", "vad_method"], VadMethodEnum.SILERO_V3.value),
            (self.ui.cbbSourceLanguage, AudioLanguageEnum, None, None,
             lambda item: self.config_set_audio_language(item)),
            (self.ui.cbbTargetLanguage, SubtitleLanguageEnum, ["translate_args", "target_language"],
             SubtitleLanguageEnum.CHINESE_SIMPLIFIED.value),
            (self.ui.cbbTranslateMode, TranslateModeEnum, ["translate_args", "translate_mode"],
             TranslateModeEnum.PRECISE.value),
            (self.ui.cbbSubtitleLayout, SubtitleLayoutEnum, ["subtitle_args", "subtitle_layout"],
             SubtitleLayoutEnum.TRANSLATE_ON_TOP.value)
        ]
        for config in combobox_configs:
            self.init_combobox(*config)

        self.ui.cbbLlmModel.currentIndexChanged.connect(
            lambda: self.on_cbbLlmModel_changed(["translate_args", "llm_model"])
        )

    def on_cbbLlmModel_changed(self, key_path: List[str]) -> None:
        """处理LLM模型下拉框变化事件。

        Args:
            key_path (List[str]): 配置字典中的键路径。
        """
        selected_value = self.ui.cbbLlmModel.currentText()
        if selected_value:
            ConfigTool.reset_config_attr(
                config_dict=self.config_args,
                key_path=key_path,
                the_value=selected_value
            )

    def on_llm_changed(self) -> None:
        """处理LLM输入框变化事件。"""
        self.llm_ok = False

    def on_select_color(self, frame: QFrame, key_path: List[str], default_color: QColor) -> None:
        """处理颜色选择事件。

        Args:
            frame (QFrame): 颜色显示框。
            key_path (List[str]): 配置字典中的键路径。
            default_color (QColor): 默认颜色。
        """
        DialogGenerator.select_and_set_color(
            parent=self.mainWindow,
            frame=frame,
            config_args=self.config_args,
            key_path=key_path,
            default_color=default_color
        )

    def write_all_config(self) -> None:
        """将UI配置写入配置文件。"""
        ConfigBinder.widget_to_config(
            widgets=self.ui.freSetting.findChildren(QWidget),
            config_args=self.config_args,
            ui_map=self.uiArgsMap
        )
        # 特殊值的处理
        self.config_args['subtitle_args']['default_style']['MarginV'] = self.config_args['subtitle_args'][
            'subtitle_margin_v']
        self.config_args['subtitle_args']['secondary_style']['MarginV'] = self.config_args['subtitle_args'][
            'subtitle_margin_v']
        self.config_args['translate_args']['llm_model'] = self.ui.cbbLlmModel.currentText()

        ConfigTool.save_config_setting(self.config_args)

    def on_check_llm_api(self) -> None:
        """检查LLM API连接状态。"""
        # if self.llm_ok:
        #     self.log_info(f"LLM 连接正常")
        #     return
        base_url = self.ui.edtBaseUrl.text()
        api_key = self.ui.edtAPiKey.text()
        llm_model = self.ui.cbbLlmModel.currentText()
        try:
            is_success, message = OpenAiChecker.test_openai(base_url=base_url, api_key=api_key, model=llm_model)
            if not is_success:
                self.llm_ok = False
                self.log_error(f"LLM 连接测试错误：{message}")
            else:
                self.llm_ok = True
                self.log_info(f"Success, LLM连接测试成功, {message}")
        except Exception as e:
            self.llm_ok = False
            self.log_error(f"LLM 连接测试发生异常", e)

    def _load_llm_models(self, base_url: str, api_key: str, current_model: str) -> None:
        """加载LLM模型列表。

        Args:
            base_url (str): LLM API的基础URL。
            api_key (str): LLM API的密钥。
            current_model (str): 当前选中的模型。
        """
        try:
            cnt = MainFrmHelper.load_llm_models(
                cbb_llm_model=self.ui.cbbLlmModel,
                base_url=base_url,
                api_key=api_key,
                config_args=self.config_args,
                current_model=current_model
            )
            if cnt > 0:
                self.log_info(f"读取LLM模型列表成功, 共 {cnt} 个模型。")
                self.llm_ok = True
        except Exception as e:
            self.log_error(f"读取LLM模型列表发生异常", e)

    def on_download_tool(self) -> None:
        """打开下载工具的URL。"""
        DialogGenerator.open_url(
            parent=self.mainWindow,
            url="https://github.com/Purfview/whisper-standalone-win/releases/tag/Faster-Whisper-XXL"
        )

    def on_download_model(self) -> None:
        """处理下载模型事件。"""
        model_name = self.ui.cbbWhisperModel.currentText()
        sub_dir = f"faster-whisper-{model_name}"
        model_path = os.path.join(self.ui.edtWhisperDir.text(), sub_dir)
        if not os.path.exists(model_path):
            os.mkdir(model_path)
        model_dir = os.path.abspath(model_path)

        url = f'https://hf-mirror.com/Systran/faster-whisper-{model_name}/tree/main'
        self.log_info(f"{model_name} 模型 \n 请手工下载这个网址上的所有文件：{url} \n"
                      f" 并保存到这个路径下: {model_dir}")

        DialogGenerator.open_url(parent=self.mainWindow, url=url)

    def on_register_llm(self) -> None:
        """打开注册LLM的URL。"""
        DialogGenerator.open_url(parent=self.mainWindow, url="https://cloud.siliconflow.cn/i/WtaGRkTP")

    def on_refresh_llm_models(self) -> None:
        self._load_llm_models(
            base_url=self.ui.edtBaseUrl.text(),
            api_key=self.ui.edtAPiKey.text(),
            current_model=self.ui.cbbLlmModel.currentText()
        )

    def on_select_whisper_exe(self) -> None:
        """选择FasterWhisper工具路径。"""
        file, _ = QFileDialog.getOpenFileName(
            parent=self.mainWindow,
            caption="选择FasterWhisper工具",
            directory=os.path.dirname(self.config_args['asr_args']['faster_whisper_path']),
            filter="*.exe"
        )
        if file:
            self.ui.edtWhisperExe.setText(file)
            self.config_args['asr_args']['faster_whisper_path'] = file

    def on_select_whisper_dir(self) -> None:
        """选择FasterWhisper模型目录。"""
        directory = QFileDialog.getExistingDirectory(
            parent=self.mainWindow,
            caption="选择目录",
            directory=self.config_args['asr_args']['model_dir']
        )
        if directory:
            self.ui.edtWhisperDir.setText(directory)
            self.config_args['asr_args']['model_dir'] = directory

    def config_set_audio_language(self, item: AudioLanguageEnum) -> None:
        """设置音频语言配置。

        Args:
            item (AudioLanguageEnum): 音频语言枚举值。
        """
        if isinstance(item, AudioLanguageEnum):
            self.config_args['asr_args']['language'] = item.code
            self.config_args['translate_args']['source_language'] = item.value

    def init_combobox(self,
                      combobox: QComboBox,
                      the_enum: Type[Enum],
                      key_path: Optional[List[str]] = None,
                      default_value: Any = None,
                      func_set_config: Optional[Callable] = None) -> None:
        """
        初始化QComboBox，填充枚举值并连接信号槽。

        Args:
            combobox (QComboBox): 要初始化的QComboBox实例。
            the_enum (Type[Enum]): 枚举类，用于填充QComboBox的选项。
            key_path (Optional[List[str]]): 配置字典中的键路径，用于更新配置。
            default_value (Any): 默认值，当键路径不存在时使用。
            func_set_config (Optional[Callable]): 设置配置的函数。
        """
        # 设置QComboBox的下拉列表项之间的间隔
        combobox.view().setSpacing(2)

        # 填充QComboBox
        for member in the_enum:
            combobox.addItem(member.value, member)

        # 连接信号和槽，当用户选择一个选项时触发
        combobox.currentIndexChanged.connect(
            lambda: self.on_combobox_changed(combobox=combobox,
                                             key_path=key_path,
                                             default_value=default_value,
                                             func_set_config=func_set_config)
        )

    def on_combobox_changed(self,
                            combobox: QComboBox,
                            key_path: Optional[List[str]] = None,
                            default_value: Any = None,
                            func_set_config: Optional[Callable] = None) -> None:
        """
        处理下拉框变化事件，更新配置字典。

        Args:
            combobox (QComboBox): QComboBox实例，其当前数据作为要设置的值。
            key_path (Optional[List[str]]): 配置字典中的键路径。
            default_value (Any): 如果键路径不存在，则使用的默认值。
            func_set_config (Optional[Callable]): 设置配置的函数。
        """
        selected_value = combobox.currentData()  # 获取下拉框当前选中的枚举值
        if func_set_config:
            func_set_config(selected_value)
        else:
            ConfigTool.reset_config_attr(config_dict=self.config_args,
                                         key_path=key_path,
                                         the_value=selected_value.value if selected_value else default_value)

    def ui_obj_enabled(self, enabled: bool) -> None:
        """
        设置UI控件的启用状态。

        Args:
            enabled (bool): 是否启用控件。
        """
        self.ui.btnStart.setEnabled(enabled)
        self.ui.btnAddFile.setEnabled(enabled)
        self.ui.btnClearFile.setEnabled(enabled)

        # 遍历所有子控件并设置启用状态
        widgets = self.ui.freSetting.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget,
                          (QPushButton, QLineEdit, QComboBox, QFontComboBox, QSpinBox, QDoubleSpinBox, QCheckBox)):
                widget.setEnabled(enabled)

    def on_save_setting(self) -> None:
        """保存当前设置到配置文件。"""
        self.write_all_config()

    def on_visible_setting(self) -> None:
        """显示或者隐藏配置信息。"""
        if self.ui.freSetting.isVisible():
            self.ui.freSetting.setVisible(False)
            self.ui.btnSettingVisible.setText("显示配置")
            self.ui.btnSettingVisible.setIcon(MainFrmHelper.build_icon(ICON_REC.get('setting-show')))
        else:
            self.ui.freSetting.setVisible(True)
            self.ui.btnSettingVisible.setText("隐藏配置")
            self.ui.btnSettingVisible.setIcon(MainFrmHelper.build_icon(ICON_REC.get('setting-hide')))

    def on_start_run(self) -> None:
        """开始运行任务前的准备工作。"""
        faster_whisper_dir = os.path.dirname(self.ui.edtWhisperExe.text())
        PathUtils.append_to_env_path(faster_whisper_dir)

        # 检查工具和模型是否准备就绪
        if self._check_tool():
            self.write_all_config()  # 将配置信息写入self.config
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
        whisper_exe = self.ui.edtWhisperExe.text()
        if not os.path.exists(whisper_exe):
            self.log_warning("Faster Whisper 没有安装。")
            return False
        self.log_info("FasterWhisper 准备就绪!")

        # 检查FasterWhisper模型是否安装
        whisper_dir = self.ui.edtWhisperDir.text()
        whisper_model = os.path.join(whisper_dir, f"faster-whisper-{self.ui.cbbWhisperModel.currentText()}")
        if not os.path.exists(whisper_dir) or not os.path.exists(whisper_model):
            self.log_warning(f"Faster Whisper 模型没有安装: {whisper_model}")
            return True  # 会自动下载
        self.log_info("FasterWhisper模型 准备就绪!")

        # 检查LLM配置是否有效
        if not self.llm_ok:
            is_success, message = OpenAiChecker.test_openai(base_url=self.ui.edtBaseUrl.text(),
                                                            api_key=self.ui.edtAPiKey.text(),
                                                            model=self.ui.cbbLlmModel.currentText())
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
            self.ui_obj_enabled(False)
            self._process_tasks(tasks)
        else:
            self.log_warning("请先选择要处理的视频文件。")

    def _process_tasks(self, tasks) -> None:
        """处理任务列表。

        Args:
            tasks: 要处理的任务列表。
        """
        self.controller.run(tasks=tasks, args=self.config_args)

    def on_all_task_finished(self) -> None:
        """所有任务完成后的处理。"""
        self.ui_obj_enabled(True)
        self.run_status = RUN_STATUS_INIT

    def on_stop_run(self) -> None:
        """停止运行任务。"""
        if self.run_status == RUN_STATUS_DOING:
            self.controller.stop()
        self.ui_obj_enabled(True)
        self.run_status = RUN_STATUS_INIT

    def on_clear_all_file(self) -> None:
        """清除所有文件。"""
        if self.run_status == RUN_STATUS_INIT:
            self.model.clear()

    def on_add_file(self) -> None:
        """显示选择文件对话框并添加文件。"""
        file_names = DialogGenerator.select_medium_files(self.mainWindow)
        if file_names:
            for file_name in file_names:
                self.model.append_row([UuidUtils.generate_guid(), Path(file_name).name, '0', '待处理', file_name])

    def build_table_view_model(self) -> ArrayTableModel:
        """构建表格视图模型。

        Returns:
            ArrayTableModel: 构建好的表格视图模型。
        """
        data = [
            ['0', '*', '0', '', '']
        ]
        headers = ['id', '名称', '进度', '步骤', '路径']
        sizes = [250, 200, 60, 200]
        return MainFrmHelper.build_tv_model(tv=self.ui.tbvTask,
                                            data=data,
                                            headers=headers,
                                            sizes=sizes)

    def run(self) -> None:
        """运行应用程序。"""
        self.mainWindow.show()
        sys.exit(self.app.exec())  # 进入程序的主循环，并通过exit函数确保主循环安全结束


if __name__ == '__main__':
    MainApp().run()
