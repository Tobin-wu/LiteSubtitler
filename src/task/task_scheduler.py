# coding: utf8
import queue
import threading
import time
from typing import Callable, Optional

from core.base_object import BaseObject


class TaskScheduler(BaseObject):
    """任务调度器类，用于管理任务的并发执行。

    该类继承自 `BaseObject`，支持任务队列管理、并发控制、进度回调以及任务中断功能。

    Attributes:
        task_queue (queue.Queue): 任务队列，用于存储待执行的任务。
        max_concurrent_tasks (int): 最大并发任务数。
        active_threads (set): 当前正在执行任务的线程集合。
        lock (threading.Lock): 线程锁，用于保护共享资源的并发访问。
        progress_callback (Callable): 进度回调函数，用于更新任务进度。
        stopped (bool): 标志位，用于中断任务调度。
    """

    def __init__(self, max_concurrent_tasks: int = 1, log_to_ui_func: Optional[Callable] = None):
        """初始化实例。

        Args:
            max_concurrent_tasks (int): 最大并发任务数，默认为 1。
            log_to_ui_func (Callable, optional): 日志输出函数，默认为 None。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self.task_queue = queue.Queue()
        self.max_concurrent_tasks = max_concurrent_tasks
        self.active_threads = set()
        self.lock = threading.Lock()
        self.progress_callback = None
        self.stopped = False

    def add_task(self, task):
        """添加任务到任务队列。

        Args:
            task: 待执行的任务对象。
        """
        self.task_queue.put(task)

    def set_progress_callback(self, callback: Callable):
        """设置进度回调函数。

        Args:
            callback (Callable): 进度回调函数，接收任务ID、进度值和执行时长。
        """
        self.progress_callback = callback

    def _update_progress(self, task_id: str, progress: int, duration: float):
        """更新任务进度并调用进度回调函数。

        Args:
            task_id (str): 任务ID。
            progress (int): 任务进度值。
            duration (float): 任务执行时长（秒）。
        """
        if self.progress_callback:
            self.progress_callback(task_id, progress, duration)

    def _task_completed(self, task):
        """任务完成后的处理逻辑。

        Args:
            task: 已完成的任务对象。
        """
        with self.lock:
            self.log_debug(f"任务（{task.task_id}）完成处理，开始下一个任务！")
            self.active_threads.discard(threading.current_thread())  # 移除当前线程

        self._start_next_task()  # 启动下一个任务

    def _start_next_task(self):
        """启动下一个任务。

        从任务队列中获取任务并启动线程执行，直到达到最大并发任务数或任务队列为空。
        """
        with self.lock:
            while len(self.active_threads) < self.max_concurrent_tasks and not self.task_queue.empty():
                if self.stopped:
                    self.log_info("收到【停止】指令，结束任务处理")
                    break

                task = self.task_queue.get()
                self.log_info(f"任务执行中：{task.task_id}")
                thread = threading.Thread(target=self._run_task, args=(task,), daemon=True)
                thread.start()
                self.active_threads.add(thread)

            if self.task_queue.empty():
                self.log_debug("任务队列为空，没有新的任务！")

    def _run_task(self, task):
        """执行任务并记录执行时长。

        Args:
            task: 待执行的任务对象。
        """
        start_time = time.time()
        task.run()  # 执行任务
        end_time = time.time()

        # 计算并记录任务执行时长
        elapsed_seconds = end_time - start_time
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.log_info(f"任务({task.task_id})执行时长: {int(hours)}小时 {int(minutes)}分钟 {seconds:.2f}秒")

        self._task_completed(task)  # 任务完成后处理

    def stop(self):
        """停止任务调度。

        设置停止标志位，中断任务调度。
        """
        self.stopped = True

    def run(self):
        """启动任务调度。

        开始从任务队列中获取任务并执行。
        """
        self._start_next_task()
