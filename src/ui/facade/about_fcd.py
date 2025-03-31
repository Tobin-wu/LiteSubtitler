# coding: utf8
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QLabel

from config import ICON_REC, APP_NAME, APP_TITLE, VERSION, APP_DESC, APP_LICENSE, AUTHOR
from core.base_object import BaseObject
from ui.driver.gui_tool import GuiTool
from ui.gui.about import Ui_dlgAbout


class AboutFacade(BaseObject):
    """About的外观类。"""

    _IMAGE_BASE_URL_ = 'https://gitee.com/tobinwu/LiteSubtitler/raw/master/docs'

    def __init__(self, func_write_log):
        """初始化LLM检测工具实例。"""
        super().__init__(log_to_ui_func=func_write_log)

        self.dialog = QDialog()
        self.ui_dialog = Ui_dlgAbout()
        self.ui_dialog.setupUi(self.dialog)

        self.ui_dialog.edtAppName.setText(f"{APP_TITLE}，{APP_NAME}")
        self.ui_dialog.edtVersion.setText(f"Version：{VERSION}")
        self.ui_dialog.edtAppDesc.setText(f"{APP_DESC}")
        self.ui_dialog.edtLicense.setText(f"开源协议：{APP_LICENSE}")

        self.ui_dialog.lblAuthorName.setText(f"联系作者：{AUTHOR}")

        target_size = QSize(201, 201)

        self.ui_dialog.lblLogo.setPixmap(QtGui.QPixmap(ICON_REC.get('logo')))
        self.ui_dialog.lblAuthor.setPixmap(QtGui.QPixmap(ICON_REC.get('author')))

        self._load_qrcode_(label=self.ui_dialog.lblService,
                           png_url=self._IMAGE_BASE_URL_ + '/使用群.png',
                           default_rec='customer_service',
                           target_size=target_size)
        self._load_qrcode_(label=self.ui_dialog.lblAiTech,
                           png_url=self._IMAGE_BASE_URL_ + '/技术群.png',
                           default_rec='ai_tech',
                           target_size=target_size)

        self.ui_dialog.btnClose.clicked.connect(lambda: self.dialog.close())

    def show(self) -> None:
        """显示。"""
        # self.dialog.setFixedHeight(580)
        self.dialog.exec()

    @staticmethod
    def _load_qrcode_(label: QLabel, png_url: str, default_rec: str, target_size):
        pixmap = GuiTool.load_image_from_url(png_url)
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(ICON_REC.get(default_rec))
        if not pixmap.isNull():
            label.setPixmap(
                pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,  # 保持宽高比
                    Qt.TransformationMode.SmoothTransformation  # 平滑缩放
                ))
        else:
            label.setText("无法加载图片")
