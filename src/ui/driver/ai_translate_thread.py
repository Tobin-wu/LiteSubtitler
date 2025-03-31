# coding: utf8
from PyQt6.QtCore import QThread, pyqtSignal

from core.asr.asr_data import ASRData
from enums.translate_mode_enum import TranslateModeEnum
from service.translate_service import TranslateService


class AiTranslateThread(QThread):
    """AI聊天中的翻译子线程"""

    message_signal = pyqtSignal(str)  # 定义信号用于传递消息
    end_signal = pyqtSignal(TranslateModeEnum, ASRData)  # 定义信号用于结束消息

    def __init__(self, service: TranslateService, asr_data: ASRData, config):
        super().__init__()
        self.is_running = True
        self.service = service
        self.asr_data = asr_data
        self._args = config
        service.reset_args(config)

    def run(self):
        import copy

        """线程执行方法"""
        self.is_running = True
        try:
            for mode in TranslateModeEnum:
                self._args['translate_mode'] = mode.value
                self.service.reset_args(self._args)
                data = self.service.translate_srt(out_file_path=None, asr_data=copy.deepcopy(self.asr_data))
                self.end_signal.emit(mode, data)
        except Exception as e:
            self.message_signal.emit(f"错误: {str(e)}\n")
        finally:
            self.is_running = False

    def stop(self):
        """停止线程"""
        self.is_running = False
        self.wait()
