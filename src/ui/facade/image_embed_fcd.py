# coding: utf8
import copy
import os.path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QWidget, QPushButton, QToolButton, QLineEdit, QComboBox, QTableView, QMessageBox

from config import ICON_REC
from core.base_object import BaseObject
from core.video.image_embed_arg import ImageEmbedArg
from enums.image_pos_enum import ImagePosEnum
from enums.supported_image_enum import SupportedImageEnum
from enums.supported_video_enum import SupportedVideoEnum
from model.file_vo import FileVO
from service.video_service import VideoService
from ui.driver.gui_tool import GuiTool
from ui.driver.image_embed_thread import ImageEmbedThread
from ui.gui.image_embed_dlg import Ui_dlgImageEmbed
from ui.gui.time_range_dlg import TimeRangeDialog
from utils.path_utils import PathUtils


class ImageEmbedFacade(BaseObject):
    """图片嵌入工具外观类，用于把图片合成到视频的首尾，把图片嵌入到视频某个时间段某个位置。"""

    def __init__(self, func_write_log, config: dict, use_cuda: bool, icon: QIcon = None):
        """初始化实例。"""
        super().__init__(log_to_ui_func=func_write_log)

        # 系统配置信息
        self.config_args = copy.deepcopy(config)
        self.use_cuda = use_cuda

        # 初始化主窗口
        self.dialog = QDialog()
        self.ui = Ui_dlgImageEmbed()
        self.ui.setupUi(self.dialog)

        if icon:
            self.dialog.setWindowIcon(icon)

        # 初始化组件映射和界面
        self._init_form_()

        # 创建视频服务对象
        self.video_service = VideoService(log_to_ui_func=func_write_log)

        # # 创建图片服务对象
        # self.image_service = ImageService(log_to_ui_func=func_write_log)

        self.video_info = None

    def show(self) -> None:
        """显示。"""
        self.dialog.exec()

    def _init_form_(self) -> None:
        """初始化窗口。"""
        self.ui.btnAddHead.clicked.connect(lambda: self._on_open_image_file_(self.ui.btnAddHead, self.ui.edtHead))
        GuiTool.setup_double_click_handler(self.ui.edtHead,
                                           lambda: self._on_open_image_file_(self.ui.btnAddHead, self.ui.edtHead))
        GuiTool.setup_double_click_handler(self.ui.lblHead,
                                           lambda: self._on_open_image_file_(self.ui.btnAddHead, self.ui.edtHead))
        self.ui.btnClearHead.clicked.connect(lambda: self._on_clear_file_(self.ui.btnClearHead, self.ui.edtHead))

        self.ui.btnAddVideo.clicked.connect(self._on_open_video_file_)
        GuiTool.setup_double_click_handler(self.ui.edtVideo, self._on_open_video_file_)
        GuiTool.setup_double_click_handler(self.ui.lblVideo, self._on_open_video_file_)

        self.ui.btnAddEmbed1.clicked.connect(lambda: self._on_open_image_file_(self.ui.btnAddEmbed1, self.ui.edtEmbed1))
        GuiTool.setup_double_click_handler(self.ui.edtEmbed1,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEmbed1, self.ui.edtEmbed1))
        GuiTool.setup_double_click_handler(self.ui.lblEmbed1,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEmbed1, self.ui.edtEmbed1))
        self.ui.btnClearEmbed1.clicked.connect(lambda: self._on_clear_file_(self.ui.btnClearEmbed1, self.ui.edtEmbed1))
        self.ui.btnEmbed1AddPeriod.clicked.connect(
            lambda: self._on_add_period_(self.ui.btnEmbed1AddPeriod, self.ui.edtEmbed1Period))
        self.ui.btnEmbed1ClearPeriod.clicked.connect(
            lambda: self._on_clear_period_(self.ui.btnEmbed1ClearPeriod, self.ui.edtEmbed1Period))

        self.ui.btnAddEmbed2.clicked.connect(lambda: self._on_open_image_file_(self.ui.btnAddEmbed2, self.ui.edtEmbed2))
        GuiTool.setup_double_click_handler(self.ui.edtEmbed2,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEmbed2, self.ui.edtEmbed2))
        GuiTool.setup_double_click_handler(self.ui.lblEmbed2,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEmbed2, self.ui.edtEmbed2))
        self.ui.btnClearEmbed2.clicked.connect(lambda: self._on_clear_file_(self.ui.btnClearEmbed2, self.ui.edtEmbed2))
        self.ui.btnEmbed2AddPeriod.clicked.connect(
            lambda: self._on_add_period_(self.ui.btnEmbed2AddPeriod, self.ui.edtEmbed2Period))
        self.ui.btnEmbed2ClearPeriod.clicked.connect(
            lambda: self._on_clear_period_(self.ui.btnClearEmbed2, self.ui.edtEmbed2Period))

        self.ui.btnAddEnd.clicked.connect(lambda: self._on_open_image_file_(self.ui.btnAddEnd, self.ui.edtEnd))
        GuiTool.setup_double_click_handler(self.ui.edtEnd,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEnd, self.ui.edtEnd))
        GuiTool.setup_double_click_handler(self.ui.lblEnd,
                                           lambda: self._on_open_image_file_(self.ui.btnAddEnd, self.ui.edtEnd))
        self.ui.btnClearEnd.clicked.connect(lambda: self._on_clear_file_(self.ui.btnClearEnd, self.ui.edtEnd))

        self.ui.btnAddOutVideo.clicked.connect(
            lambda: self._on_save_video_file_(self.ui.btnAddOutVideo, self.ui.edtOutVideo))
        GuiTool.setup_double_click_handler(self.ui.edtOutVideo,
                                           lambda: self._on_save_video_file_(self.ui.btnAddOutVideo,
                                                                             self.ui.edtOutVideo))
        GuiTool.setup_double_click_handler(self.ui.lblOutVideo,
                                           lambda: self._on_save_video_file_(self.ui.btnAddOutVideo,
                                                                             self.ui.edtOutVideo))

        self.ui.btnRun.setIcon(GuiTool.build_icon(ICON_REC.get('run')))
        self.ui.btnRun.clicked.connect(self._on_run_embed_)

    def _on_save_video_file_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit):
        if not sender.isEnabled():
            return

        default_file = ''
        if self.video_info:
            default_file = os.path.join(self.video_info['file_dir'],
                                        self.video_info['file_only_name'] + '-out.mp4')

        file_path = GuiTool.save_dialog(parent=self.dialog,
                                        default_path=str(default_file),
                                        filter_str="MP4 Files (*.mp4)")
        if file_path:
            edt_obj.setText(file_path)

    def _on_clear_period_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit):
        if not sender.isEnabled():
            return
        edt_obj.setText("")

    def _on_add_period_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit):
        if not sender.isEnabled():
            return

        new_period = self._get_period_()

        if new_period:
            txt = edt_obj.text()
            if txt:
                edt_obj.setText(txt + "+" + new_period)
            else:
                edt_obj.setText(new_period)

    def _get_period_(self):
        if self.video_info and self.video_info["duration_seconds"] and self.video_info["duration_seconds"] > 0:
            return TimeRangeDialog.get_time_range(self.video_info["duration_seconds"])
        return None

    def _on_open_image_file_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit):
        title = "打开图片文件"
        filter_str = SupportedImageEnum.filter_formats()
        return self._on_open_file_(sender, edt_obj, title, filter_str)

    def _on_clear_file_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit):
        if not sender.isEnabled():
            return

        edt_obj.setText("")

    def _on_open_file_(self, sender: QPushButton | QToolButton, edt_obj: QLineEdit, title: str, filter_str: str):
        if not sender.isEnabled():
            return

        GuiTool.open_and_select_file(parent=self.dialog,
                                     caption=title,
                                     filter_str=filter_str,
                                     file_edit=edt_obj)

    def _on_open_video_file_(self) -> None:
        """打开视频文件。"""
        if not self.ui.btnAddVideo.isEnabled():
            return
        old_video = self.ui.edtVideo.text()
        GuiTool.open_and_select_file(parent=self.dialog,
                                     caption="选择视频文件",
                                     filter_str=SupportedVideoEnum.filter_formats(),
                                     file_edit=self.ui.edtVideo)
        new_video = self.ui.edtVideo.text()
        if old_video != new_video:
            video_info = self.video_service.get_video_info(new_video)
            self.log_info(f"视频信息：{video_info}")
            if video_info['duration_seconds'] > 0:
                self.video_info = video_info
                str_info = (f'分辨率：{video_info["width"]} * {video_info["height"]})，'
                            f'时长：{video_info["duration_seconds"]} 秒')
                self.ui.lblVideoInfo.setText(str_info)
                info = FileVO(new_video)
                self.video_info['file_dir'] = info.file_dir
                self.video_info['file_only_name'] = info.file_only_name
                self.video_info['file_path'] = new_video

    def _on_run_embed_(self) -> None:
        """执行合成处理（把字幕嵌入到视频文件）。"""
        if self._check_and_refresh_():
            self._ui_obj_enabled(False)

            thread = ImageEmbedThread(service=self.video_service,
                                      config=self.config_args,
                                      video_info=self.video_info,
                                      use_cuda=self.use_cuda)
            thread.message_signal.connect(lambda msg: self.log_info(msg))
            thread.end_signal.connect(self._when_end_embed_)
            thread.start()

    def _check_path_space_(self, file_path: str, title: str):
        if file_path:
            if PathUtils.have_space(file_path):
                QMessageBox.warning(self.dialog, "异常", title)
                return False
        return True

    def _check_and_refresh_(self):
        self.config_args["head_image"] = {}
        self.config_args["head_image"]["file_path"] = self.ui.edtHead.text()
        self.config_args["head_image"]["seconds"] = self.ui.spbHeadSeconds.value()
        if not (self._check_path_space_(self.config_args["head_image"]["file_path"], '片头图片路径中不能有空格！')):
            return False

        if not self.video_info:
            QMessageBox.warning(self.dialog, "异常", "必须选择“视频文件”！")
            return False
        if not (self._check_path_space_(self.video_info['file_path'], '视频文件路径中不能有空格！')):
            return False

        embed1_overlays = ImageEmbedArg.read_pos_overlay(
            pos=ImagePosEnum.read_by_text(self.ui.cbbEmbed1Pos.currentText()),
            offset_width=self.ui.spbEmbed1PosWidth.value(),
            offset_height=self.ui.spbEmbed1PosHeight.value()).split(":")
        embed1_arg = ImageEmbedArg(
            file_path=self.ui.edtEmbed1.text(),
            scale=f'{self.ui.spbEmbed1Width.value()}:{self.ui.spbEmbed1Height.value()}',
            color_channel_mixer=self.ui.spbEmbed1Transparency.value(),
            overlay_width=embed1_overlays[0],
            overlay_height=embed1_overlays[1],
            enable_time_period=self.ui.edtEmbed1Period.text()
        )
        self.config_args["embed1_arg"] = embed1_arg
        if embed1_arg.file_path:
            if not embed1_arg.enable_time_period:
                QMessageBox.warning(self.dialog, "异常", "嵌入图-1的时段必须设置！")
                return False
            if not (self._check_path_space_(embed1_arg.file_path, '嵌入图-1路径中不能有空格！')):
                return False

        embed2_overlays = ImageEmbedArg.read_pos_overlay(
            pos=ImagePosEnum.read_by_text(self.ui.cbbEmbed2Pos.currentText()),
            offset_width=self.ui.spbEmbed2PosWidth.value(),
            offset_height=self.ui.spbEmbed2PosHeight.value()).split(":")
        embed2_arg = ImageEmbedArg(
            file_path=self.ui.edtEmbed2.text(),
            scale=f'{self.ui.spbEmbed2Width.value()}:{self.ui.spbEmbed2Height.value()}',
            color_channel_mixer=self.ui.spbEmbed2Transparency.value(),
            overlay_width=embed2_overlays[0],
            overlay_height=embed2_overlays[1],
            enable_time_period=self.ui.edtEmbed2Period.text()
        )
        self.config_args["embed2_arg"] = embed2_arg
        if embed2_arg.file_path:
            if not embed2_arg.enable_time_period:
                QMessageBox.warning(self.dialog, "异常", "嵌入图-2的时段必须设置！")
                return False
            if not (self._check_path_space_(embed2_arg.file_path, '嵌入图-2路径中不能有空格！')):
                return False

        self.config_args["end_image"] = {}
        self.config_args["end_image"]["file_path"] = self.ui.edtEnd.text()
        self.config_args["end_image"]["seconds"] = self.ui.spbEndSeconds.value()
        if not (self._check_path_space_(self.config_args["end_image"]["file_path"], '片尾图片路径中不能有空格！')):
            return False

        self.config_args["out_video"] = {}
        self.config_args["out_video"]["file_path"] = self.ui.edtOutVideo.text()
        if not self.config_args["out_video"]["file_path"]:
            QMessageBox.warning(self.dialog, "异常", "必须设置“输出视频”文件！")
            return False
        if not (self._check_path_space_(self.config_args["out_video"]["file_path"], '输出视频路径中不能有空格！')):
            return False

        self.config_args["delete_temp"] = self.ui.chbDeleteTemp.isChecked()

        path = self.config_args["head_image"]["file_path"] or \
            self.config_args["embed1_arg"].file_path or \
            self.config_args["embed2_arg"].file_path or \
            self.config_args["end_image"]["file_path"]

        if not path:
            QMessageBox.warning(self.dialog, "异常", "必须选择某个图片来进行处理！")
            return False

        return True

    def _when_end_embed_(self, msg: str):
        self._ui_obj_enabled(True)
        self.log_info(msg)

    def _ui_obj_enabled(self, enabled: bool) -> None:
        """
        设置UI控件的启用状态。

        Args:
            enabled (bool): 是否启用控件。
        """
        GuiTool.set_ui_enabled(self.ui.freHead.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freVideo.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freEmbed1.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freEmbed1Arg.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freEmbed2.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freEmbed2Arg.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freEnd.findChildren(QWidget), enabled)
        GuiTool.set_ui_enabled(self.ui.freOutVideo.findChildren(QWidget), enabled)
