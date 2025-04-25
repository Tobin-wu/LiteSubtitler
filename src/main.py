# coding: utf8
import ctypes
import os
import sys

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from config import APP_NAME, RESOURCE_PATH
from core.base_object import BaseObject
from ui.facade.main_fcd import MainFacade

# 设置应用程序的用户模型ID，以确保任务栏图标显示正确
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)


class MainApp(BaseObject):
    """主应用程序类，负责初始化界面、处理用户交互和任务调度。"""

    def __init__(self):
        """初始化实例。"""
        super().__init__()

        # 初始化Qt应用程序
        self.app = QApplication(sys.argv)
        # 加载样式表
        self._load_qss_()

        self.main_facade = MainFacade()

        # 设置应用程序的ICON图标
        self.app_icon = self._load_app_logo_()
        self.main_facade.set_app_icon(self.app_icon)

    def _load_app_logo_(self) -> QIcon | None:
        """加载应用程序图标。"""
        ico_file = os.path.join(RESOURCE_PATH, "images", "icons", "logo-32.ico")
        if os.path.exists(ico_file):
            icon = QIcon(ico_file)
            self.app.setWindowIcon(icon)
            return icon
        else:
            self.log_warning(f"图标文件缺失：{ico_file}")
        return None

    def _load_qss_(self) -> None:
        """加载QSS样式文件。"""
        qss_file = os.path.join(RESOURCE_PATH, "styles", "main.qss")
        if os.path.exists(qss_file):
            file = QFile(qss_file)
            if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                self.app.setStyleSheet(QTextStream(file).readAll())
        else:
            self.log_warning(f"样式文件缺失：{qss_file}")

    def run(self) -> None:
        """运行应用程序。"""
        self.main_facade.show_main_form()
        sys.exit(self.app.exec())  # 进入程序的主循环，并通过exit函数确保主循环安全结束


if __name__ == '__main__':
    MainApp().run()
