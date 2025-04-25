# coding: utf8
from typing import Tuple


class ASRDataSeg:
    def __init__(self, text: str, start_time: int, end_time: int):
        """
        初始化 ASRDataSeg 实例。

        Args:
            text: 文本内容
            start_time: 开始时间（毫秒）
            end_time: 结束时间（毫秒）
        """
        self.text = text
        self.start_time = start_time
        self.end_time = end_time

    def contains(self, pos: int) -> bool:
        return self.start_time <= pos < self.end_time

    def to_srt_ts(self) -> str:
        """
        转换为 SRT 时间戳格式。

        Returns:
            str: SRT时间戳字符串。
        """
        return f"{self._ms_to_srt_time(self.start_time)} --> {self._ms_to_srt_time(self.end_time)}"

    def to_lrc_ts(self) -> str:
        """
        转换为 LRC 时间戳格式。

        Returns:
            str: LRC时间戳字符串。
        """
        return f"[{self._ms_to_lrc_time(self.start_time)}]"

    def to_ass_ts(self) -> Tuple[str, str]:
        """
        转换为 ASS 时间戳格式。

        Returns:
            Tuple[str, str]: (开始时间, 结束时间) 的元组，格式为 ASS 时间戳。
        """
        return self._ms_to_ass_ts(self.start_time), self._ms_to_ass_ts(self.end_time)

    @staticmethod
    def _ms_to_lrc_time(ms: int) -> str:
        """
        将毫秒转换为 LRC 时间格式 (MM:SS.ss)

        Args:
            ms: 毫秒。
        Returns:
            str: LRC时间字符串。
        """
        seconds = ms / 1000
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{seconds:.2f}"

    @staticmethod
    def _ms_to_srt_time(ms: int) -> str:
        """
        将毫秒转换为 SRT 时间格式 (HH:MM:SS,mmm)。

        Args:
            ms: 毫秒。
        Returns:
            str: SRT时间字符串。
        """
        total_seconds, milliseconds = divmod(ms, 1000)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

    @staticmethod
    def _ms_to_ass_ts(ms: int) -> str:
        """
        将毫秒转换为 ASS 时间戳格式 (H:MM:SS.cc)


        Args:
            ms: 毫秒。
        Returns:
            str: ASS时间字符串。
        """
        total_seconds, milliseconds = divmod(ms, 1000)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        centi_seconds = int(milliseconds / 10)
        return f"{int(hours):01}:{int(minutes):02}:{int(seconds):02}.{centi_seconds:02}"

    @property
    def transcript(self) -> str:
        """
        返回分段文本。

        Returns:
            str: 文本内容。
        """
        return self.text

    def __str__(self) -> str:
        return f"ASRDataSeg({self.text}, {self.start_time}, {self.end_time})"
