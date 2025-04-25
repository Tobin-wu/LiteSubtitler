# coding: utf8
import logging
from typing import Optional, Callable

from PyQt6.QtCore import QObject, pyqtSignal

from settings.logger import setup_logger


class BaseObject(QObject):
    """
    基础对象类，提供日志功能和信号用于日志输出到 UI。

    主要功能：
        1. 提供日志记录功能，支持不同级别的日志（INFO、DEBUG、WARNING、ERROR）。
        2. 支持将日志信息通过信号传递到 UI 进行显示。
    """

    # 日志记录器，懒加载
    logger: Optional[logging.Logger] = None

    # 用于 UI 日志输出的信号
    ui_log_signal = pyqtSignal(str, str, int)  # 参数：消息、类名、日志级别

    def __init__(self, parent: Optional[QObject] = None, log_to_ui_func: Optional[Callable] = None):
        """
        初始化基础对象。

        Args:
            parent: 父对象，用于 Qt 对象树管理。
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(parent=parent)
        self.log_to_ui_func = log_to_ui_func
        if log_to_ui_func:
            self.ui_log_signal.connect(log_to_ui_func)

    def _get_logger(self) -> logging.Logger:
        """
        懒加载日志记录器。

        Returns:
            日志记录器实例。
        """
        if self.logger is None:
            self.logger = setup_logger(self.__class__.__name__)
        return self.logger

    def log_info(self, msg: str, *args, **kwargs):
        """
        记录信息日志。

        Args:
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        self._log(logging.INFO, msg, *args, **kwargs)

    def log_error(self, msg: str, *args, **kwargs):
        """
        记录错误日志。

        Args:
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        self._log(logging.ERROR, msg, *args, **kwargs)

    def log_exception(self, msg: str, *args, **kwargs):
        """
        记录异常日志，并包含异常堆栈信息。

        Args:
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        logger = self._get_logger()
        logger.error(msg, *args, exc_info=True, **kwargs)
        self._log_to_ui(msg, logging.ERROR)

    def log_debug(self, msg: str, *args, **kwargs):
        """
        记录调试日志。

        Args:
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def log_warning(self, msg: str, *args, **kwargs):
        """
        记录警告日志。

        Args:
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        self._log(logging.WARNING, msg, *args, **kwargs)

    def _log(self, level: int, msg: str, *args, **kwargs):
        """
        内部方法，用于记录日志并输出到 UI。

        Args:
            level: 日志级别（如 logging.INFO、logging.ERROR 等）。
            msg: 日志消息。
            *args: 格式化参数。
            **kwargs: 其他关键字参数。
        """
        logger = self._get_logger()
        logger.log(level, msg, *args, **kwargs)
        self._log_to_ui(msg, level)

    def _log_to_ui(self, msg: str, level: int):
        """
        将日志消息通过信号传递到 UI。

        Args:
            msg: 日志消息。
            level: 日志级别。
        """
        if self.log_to_ui_func:
            self.ui_log_signal.emit(msg, self.__class__.__name__, level)