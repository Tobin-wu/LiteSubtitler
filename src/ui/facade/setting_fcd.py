# coding: utf8
import os
from enum import Enum
from typing import Type, Any, List, Optional, Callable

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QComboBox, QFrame, QWidget, QDialog

from config import ConfigTool, ICON_REC, FASTER_WHISPER_URL, LLM_ACCOUNT_URL
from core.llm.opanai_checker import OpenAiChecker
from enums.faster_whisper_enums import FasterWhisperModelEnum, FasterWhisperDeviceEnum, VadMethodEnum
from enums.language_enums import AudioLanguageEnum, SubtitleLanguageEnum
from enums.supported_subtitle_enum import SubtitleLayoutEnum
from enums.translate_mode_enum import TranslateModeEnum
from model.unique_key_value_map import UniqueKeyValueMap
from ui.base_config_facade import BaseConfigFacade
from ui.driver.gui_tool import GuiTool
from ui.gui.setting_dlg import Ui_dlgSetting


class SettingFacade(BaseConfigFacade):
    """配置外观类，用于调整系统配置信息。"""

    def __init__(self, func_write_log, config):
        """初始化应用程序实例。"""
        super().__init__(log_to_ui_func=func_write_log, config=config)

        # 初始化主窗口
        self.dialog = QDialog()
        self.ui = Ui_dlgSetting()
        self.ui.setupUi(self.dialog)

        # 初始化组件映射和界面
        self.uiArgsMap = self._read_ui_and_args_map_()
        self._init_form_()

    def show(self) -> None:
        """显示。"""
        self.dialog.exec()

    def _init_form_(self) -> None:
        """初始化主窗口界面组件。"""
        self._fill_icon_()
        # 组件初始化和数据绑定
        self._init_form_comp_()
        self._fill_args_to_ui()

    def _read_ui_and_args_map_(self) -> UniqueKeyValueMap:
        """创建UI组件与配置键的映射关系。

        Returns:
            UniqueKeyValueMap: UI组件与配置键的映射关系。
        """
        ui = self.ui
        ui_map = UniqueKeyValueMap()

        # ASR相关参数映射
        ui_map.add(("asr_args", "faster_whisper_path"), ui.edtWhisperExe.objectName())
        ui_map.add(("asr_args", "whisper_model"), ui.cbbWhisperModel.objectName())
        ui_map.add(("asr_args", "model_dir"), ui.edtWhisperDir.objectName())
        ui_map.add(("asr_args", "device"), ui.cbbRunDevice.objectName())
        ui_map.add(("asr_args", "ff_mdx_kim2"), ui.ckbHumanVoice.objectName())
        ui_map.add(("asr_args", "vad_filter"), ui.ckbVad.objectName())
        ui_map.add(("asr_args", "vad_method"), ui.cbbVadMethod.objectName())
        ui_map.add(("asr_args", "vad_threshold"), ui.spbVadValue.objectName())

        # 翻译相关参数映射
        ui_map.add(("translate_args", "need_translate"), ui.ckbTranslate.objectName())
        ui_map.add(("translate_args", "need_remove_punctuation"), ui.ckbClearPunctuation.objectName())
        ui_map.add(("translate_args", "translate_mode"), ui.cbbTranslateMode.objectName())
        ui_map.add(("translate_args", "source_language"), ui.cbbSourceLanguage.objectName())
        ui_map.add(("translate_args", "target_language"), ui.cbbTargetLanguage.objectName())
        ui_map.add(("translate_args", "llm_api_key"), ui.edtAPiKey.objectName())
        ui_map.add(("translate_args", "llm_api_url"), ui.edtBaseUrl.objectName())
        ui_map.add(("translate_args", "llm_model"), ui.cbbLlmModel.objectName())

        # 字幕相关参数映射
        ui_map.add(("subtitle_args", "need_remove_temp_file"), ui.ckbRemoveTempFile.objectName())
        ui_map.add(("subtitle_args", "is_embed_subtitle"), ui.ckbEmbedSubtitle.objectName())
        ui_map.add(("subtitle_args", "is_soft_subtitle"), ui.ckbSoftSubtitle.objectName())
        ui_map.add(("subtitle_args", "subtitle_layout"), ui.cbbSubtitleLayout.objectName())
        ui_map.add(("subtitle_args", "subtitle_margin_v"), ui.spbSubtitleVH.objectName())

        # 字幕默认样式映射
        ui_map.add(("subtitle_args", "default_style", "Fontname"), ui.cbbMainFont.objectName())
        ui_map.add(("subtitle_args", "default_style", "Fontsize"), ui.spbMainSize.objectName())
        ui_map.add(("subtitle_args", "default_style", "Spacing"), ui.spbMainSpacing.objectName())
        ui_map.add(("subtitle_args", "default_style", "PrimaryColour"), ui.freMainColor.objectName())
        ui_map.add(("subtitle_args", "default_style", "OutlineColour"), ui.freMainOutlineColor.objectName())

        # 字幕次要样式映射
        ui_map.add(("subtitle_args", "secondary_style", "Fontname"), ui.cbbSecondFont.objectName())
        ui_map.add(("subtitle_args", "secondary_style", "Fontsize"), ui.spbSecondSize.objectName())
        ui_map.add(("subtitle_args", "secondary_style", "Spacing"), ui.spbSecondSpacing.objectName())
        ui_map.add(("subtitle_args", "secondary_style", "PrimaryColour"), ui.freSecondColor.objectName())
        ui_map.add(("subtitle_args", "secondary_style", "OutlineColour"), ui.freSecondOutlineColor.objectName())

        return ui_map

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
        GuiTool.fill_widget(
            widgets=self.ui.freSetting.findChildren(QWidget),
            config_args=self.config_args,
            ui_map=self.uiArgsMap
        )

    def _fill_icon_(self):
        """为UI中的按钮设置图标。"""
        ui = self.ui

        # 设置按钮图标
        ui.btnSetting.setIcon(GuiTool.build_icon(ICON_REC.get('ok')))

        ui.btnDownTool.setIcon(GuiTool.build_icon(ICON_REC.get('download')))
        ui.btnDownModel.setIcon(GuiTool.build_icon(ICON_REC.get('download-model')))
        ui.btnLlmApi.setIcon(GuiTool.build_icon(ICON_REC.get('register-llm')))
        ui.btnLlmRefresh.setIcon(GuiTool.build_icon(ICON_REC.get('refresh')))
        ui.btnWhisperExe.setIcon(GuiTool.build_icon(ICON_REC.get('file')))
        ui.btnWhisperDir.setIcon(GuiTool.build_icon(ICON_REC.get('dir')))
        ui.btnCheckApi.setIcon(GuiTool.build_icon(ICON_REC.get('link')))

        # 设置颜色选择按钮的图标
        icon = GuiTool.build_icon(ICON_REC.get('color'))
        ui.btnMainColor.setIcon(icon)
        ui.btnMainOutlineColor.setIcon(icon)
        ui.btnSecondColor.setIcon(icon)
        ui.btnSecondOutlineColor.setIcon(icon)

    def _init_form_comp_(self) -> None:
        """初始化界面组件和事件绑定。"""
        # 按钮事件绑定
        buttons = [
            (self.ui.btnSetting, self._on_save_setting),
            (self.ui.btnDownTool, lambda: self._on_open_url_(FASTER_WHISPER_URL)),
            (self.ui.btnDownModel, self._on_download_model),
            (self.ui.btnLlmApi, lambda: self._on_open_url_(LLM_ACCOUNT_URL)),
            (self.ui.btnLlmRefresh, self._on_refresh_llm_models),
            (self.ui.btnWhisperExe, self._on_select_whisper_exe),
            (self.ui.btnWhisperDir, self._on_select_whisper_dir),
            (self.ui.btnCheckApi, self._on_check_llm_api),
            (self.ui.btnCancel, self._on_cancel_)
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
            btn.clicked.connect(lambda _, f=fre, p=path, c=color: self._on_select_color(f, p, c))

        enable_languages = self._read_enable_languages_()

        # 初始化下拉框
        combobox_configs = [
            (self.ui.cbbWhisperModel, FasterWhisperModelEnum, ["asr_args", "whisper_model"],
             FasterWhisperModelEnum.LARGE_V2.value),
            (self.ui.cbbRunDevice, FasterWhisperDeviceEnum, ["asr_args", "device"], FasterWhisperDeviceEnum.CPU.value),
            (self.ui.cbbVadMethod, VadMethodEnum, ["asr_args", "vad_method"], VadMethodEnum.SILERO_V3.value),
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

        self.ui.cbbLlmModel.currentIndexChanged.connect(
            lambda: self._on_cbbLlmModel_changed(["translate_args", "llm_model"])
        )

    def _on_open_url_(self, url) -> None:
        """打开指定的URL。"""
        GuiTool.open_url(parent=self.dialog, url=url)

    def _read_enable_languages_(self) -> list[str]:
        if "SHOW_LANGUAGES" in self.config_args:
            if "enabled" in self.config_args["SHOW_LANGUAGES"]:
                if self.config_args["SHOW_LANGUAGES"]["enabled"]:
                    if "languages" in self.config_args["SHOW_LANGUAGES"]:
                        return self.config_args["SHOW_LANGUAGES"]["languages"]
        return [member.value for member in SubtitleLanguageEnum]

    def _on_cbbLlmModel_changed(self, key_path: List[str]) -> None:
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

    def _on_select_color(self, frame: QFrame, key_path: List[str], default_color: QColor) -> None:
        """处理颜色选择事件。

        Args:
            frame (QFrame): 颜色显示框。
            key_path (List[str]): 配置字典中的键路径。
            default_color (QColor): 默认颜色。
        """
        GuiTool.select_and_set_color(
            parent=self.dialog,
            frame=frame,
            config_args=self.config_args,
            key_path=key_path,
            default_color=default_color
        )

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
        self.config_args['translate_args']['llm_model'] = self.ui.cbbLlmModel.currentText()

        ConfigTool.save_config_setting(self.config_args)

    def _on_check_llm_api(self) -> None:
        """检查LLM API连接状态。"""
        base_url = self.ui.edtBaseUrl.text()
        api_key = self.ui.edtAPiKey.text()
        llm_model = self.ui.cbbLlmModel.currentText()
        try:
            is_success, message = OpenAiChecker.test_openai(base_url=base_url, api_key=api_key, model=llm_model)
            if not is_success:
                self.log_error(f"LLM 连接测试错误：{message}")
            else:
                self.log_info(f"Success, LLM连接测试成功, {message}")
        except Exception as e:
            self.log_error(f"LLM 连接测试发生异常", e)

    def _load_llm_models(self, base_url: str, api_key: str, current_model: str) -> None:
        """加载LLM模型列表。

        Args:
            base_url (str): LLM API的基础URL。
            api_key (str): LLM API的密钥。
            current_model (str): 当前选中的模型。
        """
        try:
            cnt = GuiTool.load_llm_models(
                cbb_llm_model=self.ui.cbbLlmModel,
                base_url=base_url,
                api_key=api_key,
                config_args=self.config_args,
                current_model=current_model
            )
            if cnt > 0:
                self.log_info(f"读取LLM模型列表成功, 共 {cnt} 个模型。")
        except Exception as e:
            self.log_error(f"读取LLM模型列表发生异常", e)

    def _on_download_model(self) -> None:
        """处理下载模型事件。"""
        model_name = self.ui.cbbWhisperModel.currentText()
        sub_dir = f"faster-whisper-{model_name}"
        model_path = os.path.join(self.ui.edtWhisperDir.text(), sub_dir)
        if not os.path.exists(model_path):
            os.makedirs(name=model_path, exist_ok=True)
        model_dir = os.path.abspath(model_path)

        url = f'https://hf-mirror.com/Systran/faster-whisper-{model_name}/tree/main'
        self.log_info(f"{model_name} 模型 \n 请手工下载这个网址上的所有文件：{url} \n"
                      f" 并保存到这个路径下: {model_dir}")

        GuiTool.open_url(parent=self.dialog, url=url)

    def _on_refresh_llm_models(self) -> None:
        self._load_llm_models(
            base_url=self.ui.edtBaseUrl.text(),
            api_key=self.ui.edtAPiKey.text(),
            current_model=self.ui.cbbLlmModel.currentText()
        )

    def _on_select_whisper_exe(self) -> None:
        """选择FasterWhisper工具路径。"""
        file, _ = QFileDialog.getOpenFileName(
            parent=self.dialog,
            caption="选择FasterWhisper工具",
            directory=os.path.dirname(self.config_args['asr_args']['faster_whisper_path']),
            filter="*.exe"
        )
        if file:
            self.ui.edtWhisperExe.setText(file)
            self.config_args['asr_args']['faster_whisper_path'] = file

    def _on_select_whisper_dir(self) -> None:
        """选择FasterWhisper模型目录。"""
        directory = QFileDialog.getExistingDirectory(
            parent=self.dialog,
            caption="选择目录",
            directory=self.config_args['asr_args']['model_dir']
        )
        if directory:
            self.ui.edtWhisperDir.setText(directory)
            self.config_args['asr_args']['model_dir'] = directory

    def _config_set_audio_language(self, item: AudioLanguageEnum) -> None:
        """设置音频语言配置。

        Args:
            item (AudioLanguageEnum): 音频语言枚举值。
        """
        if isinstance(item, AudioLanguageEnum):
            self.config_args['asr_args']['language'] = item.code
            self.config_args['translate_args']['source_language'] = item.value

    def _on_save_setting(self) -> None:
        """保存当前设置到配置文件。"""
        self._write_all_config()
        self.dialog.close()

    def _on_cancel_(self):
        self.dialog.close()
