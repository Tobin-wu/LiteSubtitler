# coding: utf8
from PyQt6.QtCore import QThread, pyqtSignal

from core.asr.asr_data import ASRData
from service.video_service import VideoService


class SubtitleEmbedThread(QThread):
    """字幕合成子线程"""

    message_signal = pyqtSignal(str)  # 定义信号用于传递消息
    end_signal = pyqtSignal(str)  # 定义信号用于结束消息

    def __init__(self, service: VideoService, asr_data: ASRData, config, video_file: str, use_cuda: bool = False):
        super().__init__()
        self.is_running = True
        self.service = service
        self.asr_data = asr_data
        self._args = config
        self.video_file = video_file
        service.reset_args(config)
        service.reset_cuda(use_cuda)

    def run(self):
        import copy

        """线程执行方法"""
        self.is_running = True
        try:
            self.message_signal.emit(f"字幕合成开始：{self.video_file}")
            self.service.reset_args(self._args)
            data = self.service.embed_subtitles(video_file_path=self.video_file,
                                                asr_data=copy.deepcopy(self.asr_data))
        except Exception as e:
            self.message_signal.emit(f"字幕合成错误: {str(e)}\n")
        finally:
            self.end_signal.emit(f"字幕合成结束:{self.video_file}")
            self.is_running = False

    def stop(self):
        """停止线程"""
        self.is_running = False
        self.wait()
