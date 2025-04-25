# coding: utf8
from PyQt6.QtCore import pyqtSignal

from core.base_object import BaseObject


class StepProcessor(BaseObject):
    """步骤处理器类，用于按顺序执行一系列步骤，并支持进度更新和中断功能。

    该类继承自 `BaseObject`，并定义了一个信号 `progress_signal`，用于传递进度信息。

    Attributes:
        progress_signal (pyqtSignal): 信号，用于传递任务ID、进度值和步骤描述。
    """
    progress_signal = pyqtSignal(str, int, str)  # 信号：传递任务ID、进度值和步骤描述

    def __init__(self, steps, parent=None, log_to_ui_func=None):
        """初始化实例。

        Args:
            steps (list): 包含步骤信息的列表，每个步骤是一个元组，格式为：
                (task_id: str, task_progress: int, step_desc: str, step_func: callable, initial_input: any)
                其中 `initial_input` 是可选的，如果某个步骤不需要初始输入，可以省略。
            parent (QObject, optional): 父对象，默认为 None。
            log_to_ui_func (callable, optional): 日志输出函数，默认为 None。
        """
        super().__init__(parent=parent, log_to_ui_func=log_to_ui_func)
        self.stopped = False  # 标志位，用于中断步骤执行
        self.steps = []  # 存储步骤的列表

        # 解析并存储步骤信息
        for step in steps:
            task_id, task_progress, step_desc, step_func, *initial_input = step
            initial_input = initial_input[0] if initial_input else None  # 处理可选的初始输入
            self.steps.append((task_id, task_progress, step_desc, step_func, initial_input))

    def run(self, initial_data=None):
        """按顺序执行步骤，并返回最终的结果。

        Args:
            initial_data (any, optional): 初始数据，将作为第一个步骤的输入（如果第一个步骤需要）。
                默认为 None。

        Returns:
            any: 最终步骤的输出结果。如果步骤被中断，返回最后一个成功步骤的输出。
        """
        current_data = initial_data
        for step in self.steps:
            if self.stopped:  # 检查是否中断
                self.log_info("步骤执行已中断")
                break

            task_id, task_progress, step_desc, step_func, initial_input = step

            # 更新进度信息
            self.progress_signal.emit(task_id, task_progress, step_desc)
            self.log_info(f'当前步骤：{step_desc}')

            # 执行步骤函数
            try:
                if initial_input is None:
                    current_data = step_func(current_data)  # 使用上一个步骤的输出作为输入
                else:
                    if current_data is None:
                        current_data = step_func(initial_input)  # 使用初始输入作为第一个步骤的输入
                    else:
                        current_data = step_func(initial_input, current_data)  # 使用初始输入和当前数据作为输入
            except Exception as e:
                self.log_error(f"步骤 '{step_desc}' 执行失败: {e}")
                raise  # 抛出异常，中断执行

        return current_data

    def stop(self):
        """中断步骤的执行。"""
        self.stopped = True
        self.log_info("步骤处理器已收到中断信号，将在当前步骤完成之后停止！")
