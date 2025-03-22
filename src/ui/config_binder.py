# coding: utf8
from PyQt6.QtWidgets import QWidget, QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QComboBox, QFontComboBox, QFrame

from config import ConfigTool
from model.unique_key_value_map import UniqueKeyValueMap
from ui.main_frm import Ui_frmMain


class ConfigBinder:
    """配置绑定器，用于将UI组件与配置数据进行绑定和同步。"""

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
                    ConfigBinder.reset_frame_color(frame=widget, color=str(value))

    @staticmethod
    def reset_frame_color(frame: QFrame, color: str):
        """重置QFrame的背景颜色。

        Args:
            frame (QFrame): 需要设置颜色的QFrame组件。
            color (str): 颜色值，可以是颜色名称或十六进制颜色代码。
        """
        frame.setStyleSheet(f"background-color: {color}; border: 1px solid black")

    @staticmethod
    def ui_and_args_map(ui: Ui_frmMain) -> UniqueKeyValueMap:
        """创建UI组件与配置键的映射关系。

        Args:
            ui (Ui_frmMain): 主界面的UI对象。

        Returns:
            UniqueKeyValueMap: UI组件与配置键的映射关系。
        """
        ui_map = UniqueKeyValueMap()

        # ASR相关参数映射
        ui_map.add(("asr_args", "faster_whisper_path"), ui.edtWhisperExe.objectName())
        ui_map.add(("asr_args", "whisper_model"), ui.cbbWhisperModel.objectName())
        ui_map.add(("asr_args", "model_dir"), ui.edtWhisperDir.objectName())
        ui_map.add(("asr_args", "device"), ui.cbbRunDevice.objectName())
        ui_map.add(("asr_args", "ff_mdx_kim2"), ui.chbHumanVoice.objectName())
        ui_map.add(("asr_args", "vad_filter"), ui.chbVad.objectName())
        ui_map.add(("asr_args", "vad_method"), ui.cbbVadMethod.objectName())
        ui_map.add(("asr_args", "vad_threshold"), ui.spbVadValue.objectName())

        # 翻译相关参数映射
        ui_map.add(("translate_args", "need_translate"), ui.chbTranslate.objectName())
        ui_map.add(("translate_args", "need_remove_punctuation"), ui.chbClearPunctuation.objectName())
        ui_map.add(("translate_args", "translate_mode"), ui.cbbTranslateMode.objectName())
        ui_map.add(("translate_args", "source_language"), ui.cbbSourceLanguage.objectName())
        ui_map.add(("translate_args", "target_language"), ui.cbbTargetLanguage.objectName())
        ui_map.add(("translate_args", "llm_api_key"), ui.edtAPiKey.objectName())
        ui_map.add(("translate_args", "llm_api_url"), ui.edtBaseUrl.objectName())
        ui_map.add(("translate_args", "llm_model"), ui.cbbLlmModel.objectName())

        # 字幕相关参数映射
        ui_map.add(("subtitle_args", "need_remove_temp_file"), ui.chbRemoveTempFile.objectName())
        ui_map.add(("subtitle_args", "is_embed_subtitle"), ui.chbEmbedSubtitle.objectName())
        ui_map.add(("subtitle_args", "is_soft_subtitle"), ui.chbSoftSubtitle.objectName())
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
