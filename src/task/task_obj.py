# coding: utf8
from core.base_object import BaseObject


class TaskObj(BaseObject):
    """任务对象类，用于封装任务的执行逻辑和完成后的回调。

    该类继承自 `BaseObject`，支持日志输出和任务完成后的回调处理。

    Attributes:
        task_id (str): 任务的唯一标识。
        finished_function (callable): 任务完成后的回调函数。
        process_function (callable): 任务的处理函数。
        args (tuple): 处理函数的可变位置参数。
        kwargs (dict): 处理函数的可变关键字参数。
    """

    def __init__(self, task_id: str, finished_function, process_function, log_to_ui_func, *args, **kwargs):
        """初始化任务对象。

        Args:
            task_id (str): 任务的唯一标识。
            finished_function (callable): 任务完成后的回调函数，接收任务ID和结束消息。
            process_function (callable): 任务的处理函数，接收任务ID和其他参数。
            log_to_ui_func (callable): 日志输出函数，用于将日志信息传递到UI。
            *args: 处理函数的可变位置参数。
            **kwargs: 处理函数的可变关键字参数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self.task_id = task_id
        self.finished_function = finished_function
        self.process_function = process_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """执行任务。

        调用处理函数执行任务逻辑，并在任务完成后调用回调函数。如果任务执行过程中发生异常，
        会记录异常信息并传递给回调函数。
        """
        msg = '正常结束'  # 默认任务结束消息
        try:
            if self.process_function:
                self.process_function(self.task_id, *self.args, **self.kwargs)  # 执行任务处理函数
            self.log_info(f'任务 {self.task_id} 正常结束')
        except Exception as e:
            msg = '处理异常!!!!'
            self.log_exception(f'任务 {self.task_id} 异常结束', e)  # 记录异常信息
        finally:
            if self.finished_function:
                self.finished_function(self.task_id, msg)  # 调用任务完成回调函数
