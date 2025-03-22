# coding: utf8
from typing import Dict, Callable, Any
from PyQt6.QtCore import QThread, pyqtSignal


class WorkThread(QThread):
    """
    工作线程类，用于在后台执行任务并通过信号与主线程通信。

    主要功能：
        1. 在后台执行任务，避免阻塞主线程。
        2. 通过信号与主线程通信，传递任务进度和结果。
    """

    # 自定义信号
    progress = pyqtSignal(str, int, str)  # 任务进度信号，参数：状态、进度、消息
    finished = pyqtSignal(object)  # 任务完成信号，参数：任务结果

    def __init__(
        self,
        task: Dict[str, str],
        process_function: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ):
        """
        初始化工作线程。

        Args:
            task: 任务信息的字典。
            process_function: 处理任务的函数。
            *args: 处理函数的参数。
            **kwargs: 处理函数的关键字参数。
        """
        super().__init__()
        self.task = task
        self.process_function = process_function
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """
        线程运行函数，在线程中调用处理函数并发送完成信号。

        如果任务执行过程中发生异常，会通过信号发送错误信息。
        """
        try:
            # 执行处理函数
            self.process_function(*self.args, **self.kwargs)
        except Exception as e:
            # 捕获异常并发送错误信息
            self.progress.emit("Error", 0, str(e))
        else:
            # 任务完成，发送完成信号
            self.finished.emit(self.task)

    def read_task(self) -> Dict[str, str]:
        """
        获取当前任务信息。

        Returns:
            任务信息的字典。
        """
        return self.task
