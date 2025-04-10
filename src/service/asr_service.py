# coding: utf8
from typing import Optional, Dict, Any
from core.asr.asr_data import ASRData
from core.base_object import BaseObject
from core.asr.faster_whisper import FasterWhisper
from core.srt.srt_segmentor import SrtSegmentor
from utils.dict_utils import DictUtils


class AsrService(BaseObject):
    """
    ASR 服务类，用于执行音频文件的自动语音识别（ASR）任务。

    主要功能：
        1. 初始化 ASR 参数并执行 ASR 识别。
        2. 合并 ASR 识别的单词为句子。
    """

    def __init__(self, log_to_ui_func: Optional[callable] = None):
        """
        初始化 ASR 服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self._args = self._init_default_args(log_to_ui_func)

    @staticmethod
    def _init_default_args(log_to_ui_func: Optional[callable]) -> Dict[str, Any]:
        """
        初始化默认的 ASR 参数。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。

        Returns:
            包含默认参数的字典。
        """
        return {
            "use_cache": False,
            "need_word_time_stamp": True,
            "faster_whisper_path": "D:/tools/ai/Faster-Whisper-XXL/faster-whisper-xxl.exe",
            "whisper_model": "large-v2",
            "model_dir": "D:/tools/ai/models",
            "device": "auto",  # cuda or cpu or auto
            "vad_filter": False,
            "vad_threshold": 0.2,
            "vad_method": "silero_v3",
            "ff_mdx_kim2": True,  # 分离出人声
            "one_word": True,
            "sentence": False,
            "language": "en",
            "prompt": "",
            "log_to_ui_func": log_to_ui_func
        }

    def reset_args(self, the_args: Dict[str, Any]) -> None:
        """
        重置 ASR 参数。

        Args:
            the_args: 包含新参数的字典。
        """
        # 更新参数，仅更新存在的键
        DictUtils.update_by_key(self._args, the_args)

        if "language" in the_args:
            self._args["language"] = None if the_args["language"] == "auto" else the_args["language"]

    def asr_process(self, out_file_path: Optional[str], audio_file_path: str) -> Optional[ASRData]:
        """
        执行 ASR 识别任务。

        Args:
            out_file_path: 输出 SRT 文件的路径。如果为 None，则不保存文件。
            audio_file_path: 音频文件的路径。

        Returns:
            ASRData 对象，包含识别结果。如果发生错误则返回 None。
        """
        self.log_info("开始 ASR 识别")
        asr_svr = FasterWhisper(audio_file_path, **self._args)
        try:
            ret_data = asr_svr.run()
            if out_file_path:
                ret_data.to_srt(layout="仅原文", save_path=out_file_path)
            ret_data.audio_file = audio_file_path
            return ret_data
        except Exception as e:
            self.log_error(f"ASR 识别失败: {e}")
            return None
        finally:
            asr_svr.stop()

    def merge_words(self, out_file_path: Optional[str], asr_data: ASRData) -> ASRData:
        """
        将 ASR 识别的单词合并为句子。

        Args:
            out_file_path: 输出 SRT 文件的路径。如果为 None，则不保存文件。
            asr_data: 包含 ASR 识别结果的 ASRData 对象。

        Returns:
            合并后的 ASRData 对象。
        """
        self.log_info("进行词 => 句子的合并")
        segmentor = SrtSegmentor(log_to_ui_func=self.log_to_ui_func)

        # 预处理 ASR 数据，移除纯标点符号的分段，并处理仅包含字母和撇号的文本
        asr_data.segments = segmentor.preprocess_segments(asr_data.segments, need_lower=False)
        asr_data.segments = segmentor.process_by_rules(asr_data.segments)
        asr_data.remove_or_add_space_for_segments()

        if out_file_path:
            asr_data.to_srt(layout="仅原文", save_path=out_file_path)

        return asr_data
