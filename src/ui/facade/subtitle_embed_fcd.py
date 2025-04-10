# coding: utf8
import copy
import os.path

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QDialog, QWidget, QPushButton, QToolButton, QLineEdit, QComboBox, QTableView

from config import ICON_REC
from core.asr.asr_data_builder import AsrDataBuilder
from core.asr.asr_data_seg import ASRDataSeg
from core.base_object import BaseObject
from enums.supported_subtitle_enum import SubtitleLayoutEnum, SupportedSubtitleEnum
from enums.supported_video_enum import SupportedVideoEnum
from model.file_vo import FileVO
from service.video_service import VideoService
from ui.driver.gui_tool import GuiTool
from ui.driver.subtitle_embed_thread import SubtitleEmbedThread
from ui.gui.subtitle_embed_dlg import Ui_dlgSubtitleEmbed
from utils.file_utils import FileUtils


class SubtitleEmbedFacade(BaseObject):
    """字幕嵌入器外观类，用于编辑字幕并执行把字幕嵌入到视频的处理。"""

    def __init__(self, func_write_log, config: dict):
        """初始化应用程序实例。"""
        super().__init__(log_to_ui_func=func_write_log)

        # 系统配置信息
        self.config_args = copy.deepcopy(config)

        # 初始化主窗口
        self.dialog = QDialog()
        self.ui = Ui_dlgSubtitleEmbed()
        self.ui.setupUi(self.dialog)

        # 初始化组件映射和界面
        self._init_form_()

        # 创建视频服务对象
        self.video_service = VideoService(log_to_ui_func=func_write_log)

        self.asr_data = None
        self.model = self._build_tableview_model_()
        self.subtitle_file_vo = None

    def show(self) -> None:
        """显示。"""
        self.dialog.exec()

    def _init_form_(self) -> None:
        """初始化主窗口界面组件。"""
        self.ui.btnVideoFile.clicked.connect(self._on_open_video_file_)
        self.ui.btnSubtitleFile.clicked.connect(self._on_open_subtitle_file_)

        self._setup_double_click_handler_(self.ui.edtVideoFile, self._on_open_video_file_)
        self._setup_double_click_handler_(self.ui.lblVideoFile, self._on_open_video_file_)

        self._setup_double_click_handler_(self.ui.edtSubtitleFile, self._on_open_subtitle_file_)
        self._setup_double_click_handler_(self.ui.lblSubtitleFile, self._on_open_subtitle_file_)

        self.ui.btnRun.setIcon(GuiTool.build_icon(ICON_REC.get('run')))
        self.ui.btnRun.clicked.connect(self._on_run_embed_)

        self.ui.btnSave.setIcon(GuiTool.build_icon(ICON_REC.get('save')))
        self.ui.btnSave.clicked.connect(self._on_save_)

        self.ui.btnSaveAs.setIcon(GuiTool.build_icon(ICON_REC.get('save-as')))
        self.ui.btnSaveAs.clicked.connect(self._on_save_as_)

        self.ui.btnExport.setIcon(GuiTool.build_icon(ICON_REC.get('export')))
        self.ui.btnExport.clicked.connect(self._on_export_to_)

        self.ui.cbbSubtitleLayout.clear()
        self.ui.cbbSubtitleLayout.view().setSpacing(2)
        for member in SubtitleLayoutEnum:
            self.ui.cbbSubtitleLayout.addItem(member.value, member)
            self.ui.cbbSubtitleLayout.setCurrentText(self.config_args['subtitle_args']['subtitle_layout'])

    @staticmethod
    def _setup_double_click_handler_(line_widget: QWidget, on_call):

        def event_filter(obj, event):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                on_call()
                return True  # 表示事件已处理
            return False

        line_widget.installEventFilter(line_widget)
        line_widget.eventFilter = event_filter

    def _on_export_to_(self):
        if self.asr_data:
            default_file = os.path.join(self.subtitle_file_vo.file_dir,
                                        self.subtitle_file_vo.file_only_name + '.txt')
            file_path = GuiTool.save_dialog(parent=self.dialog,
                                            default_path=str(default_file),
                                            filter_str="Text Files (*.txt)")
            if file_path:
                layout = self.ui.cbbSubtitleLayout.currentText()
                self._tableview_to_asrdata_(layout)

                result = []
                for n, seg in enumerate(self.asr_data.segments, 1):
                    result.append(f"{seg.text}\n")

                FileUtils.write_text(
                    file_path=file_path,
                    text="\n".join(result)
                )
                self.log_info(f"导出台词到：{file_path}")

    def _on_save_as_(self):
        if self.asr_data:
            default_file = os.path.join(self.subtitle_file_vo.file_dir,
                                        self.subtitle_file_vo.file_only_name + '-new.srt')

            file_path = GuiTool.save_dialog(parent=self.dialog,
                                            default_path=str(default_file),
                                            filter_str="SRT Files (*.srt)")
            if file_path:
                layout = self.ui.cbbSubtitleLayout.currentText()
                self._tableview_to_asrdata_(layout)
                self.asr_data.to_srt(save_path=file_path, layout=layout)
                self.log_info(f"另存字幕到：{file_path}")

    def _on_save_(self):
        if self.asr_data:
            layout = self.ui.cbbSubtitleLayout.currentText()
            self._tableview_to_asrdata_(layout)
            file_path = self.subtitle_file_vo.file_path
            self.asr_data.to_srt(save_path=file_path, layout=layout)
            self.log_info(f"保存字幕到：{file_path}")

    def _on_open_video_file_(self) -> None:
        """打开视频文件。"""
        if not self.ui.btnVideoFile.isEnabled():
            return

        GuiTool.open_and_select_file(parent=self.dialog,
                                     caption="选择视频文件",
                                     filter_str=SupportedVideoEnum.filter_formats(),
                                     file_edit=self.ui.edtVideoFile)

    def _on_open_subtitle_file_(self) -> None:
        """打开字幕文件。"""
        if not self.ui.btnSubtitleFile.isEnabled():
            return

        file = GuiTool.open_and_select_file(parent=self.dialog,
                                            caption="选择字幕文件",
                                            filter_str=SupportedSubtitleEnum.filter_formats(),
                                            file_edit=self.ui.edtSubtitleFile)
        if file:
            # 加载文件内容到列表中
            self.asr_data = AsrDataBuilder.from_subtitle_file(file)
            self._reset_subtitle_tableview_()
            self.subtitle_file_vo = FileVO(file)

    def _build_tableview_model_(self):
        data = [
            ['0', '-', '-', '*', '-']
        ]
        headers = ['序号', '开始时间', '结束时间', '源字幕', '翻译字幕']
        sizes = [80, 100, 100, 400]
        model = GuiTool.build_tv_model(tv=self.ui.tbvSubtitle,
                                       data=data,
                                       headers=headers,
                                       sizes=sizes)
        if model:
            model.set_editable_columns([3, 4])

        return model

    def _reset_subtitle_tableview_(self):
        """构建表格视图模型。"""
        if self.asr_data:
            self.model.clear()
            for i, seg in enumerate(self.asr_data.segments):
                if "\n" in seg.transcript:
                    original, translated = seg.transcript.split("\n", 1)
                else:
                    original, translated = seg.transcript, ""
                self.model.append_row([str(i), seg.start_time, seg.end_time, original, translated])

    def _on_run_embed_(self) -> None:
        """执行合成处理（把字幕嵌入到视频文件）。"""
        if self.asr_data:
            self._ui_obj_enabled(False)
            self.config_args['subtitle_args']['subtitle_layout'] = self.ui.cbbSubtitleLayout.currentText()
            self._tableview_to_asrdata_(self.config_args['subtitle_args']['subtitle_layout'])
            video_file = self.ui.edtVideoFile.text()
            thread = SubtitleEmbedThread(service=self.video_service,
                                         asr_data=copy.deepcopy(self.asr_data),
                                         config=self.config_args['subtitle_args'],
                                         video_file=video_file)
            thread.message_signal.connect(lambda msg: self.log_info(msg))
            thread.end_signal.connect(self._when_end_embed_)
            thread.start()

    def _when_end_embed_(self, msg: str):
        self._ui_obj_enabled(True)
        self.log_info(msg)

    def _ui_obj_enabled(self, enabled: bool) -> None:
        """
        设置UI控件的启用状态。

        Args:
            enabled (bool): 是否启用控件。
        """
        def set_ui_enabled(widgets):
            # 遍历所有子控件并设置启用状态
            for widget in widgets:
                if isinstance(widget,
                              (QPushButton, QToolButton, QLineEdit, QComboBox, QTableView)):
                    widget.setEnabled(enabled)
        set_ui_enabled(self.ui.freTools.findChildren(QWidget))
        set_ui_enabled(self.ui.freSubtitle.findChildren(QWidget))
        set_ui_enabled(self.ui.freVideo.findChildren(QWidget))
        self.ui.tbvSubtitle.setEnabled(enabled)

    def _tableview_to_asrdata_(self, layout: str):
        if self.model:
            segments = []
            for subtitle in self.model.data:
                # id = subtitle[0]
                start_time = subtitle[1]
                end_time = subtitle[2]
                source_msg = subtitle[3].replace("\n", "")
                translate_msg = subtitle[4].replace("\n", "")
                if SubtitleLayoutEnum.ONLY_TRANSLATE.value == layout:
                    text = translate_msg
                elif SubtitleLayoutEnum.ONLY_ORIGINAL.value == layout:
                    text = source_msg
                elif SubtitleLayoutEnum.ORIGINAL_ON_TOP.value == layout:
                    text = f'{source_msg}\n{translate_msg}'
                elif SubtitleLayoutEnum.TRANSLATE_ON_TOP.value == layout:
                    text = f'{translate_msg}\n{source_msg}'
                else:
                    text = source_msg
                segments.append(ASRDataSeg(text, start_time, end_time))
            self.asr_data.segments = segments
