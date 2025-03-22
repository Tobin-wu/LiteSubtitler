# coding: utf8
import os
from typing import LiteralString, Union, Optional
from core.audio.audio_tool import AudioTool
from core.base_object import BaseObject
from model.file_vo import FileVO


class AudioService(BaseObject):
    """
    音频服务类，用于处理音频文件的格式转换和元数据读取。

    主要功能：
        1. 将音频文件转换为指定格式（如 MP3、WAV）。
        2. 读取 WAV 文件的时长。
    """

    def __init__(self, log_to_ui_func: Optional[callable] = None):
        """
        初始化音频服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)

    def convert_to_mp3(self, audio_file_vo: FileVO) -> Union[LiteralString, str, bytes]:
        """
        将音频文件转换为 MP3 格式。

        Args:
            audio_file_vo: 音频文件的值对象。

        Returns:
            转换后的音频文件路径。
        """
        return self.convert_for_fmt(audio_file_vo=audio_file_vo, format_flag='mp3')

    def convert_to_wav(self, audio_file_vo: FileVO) -> Union[LiteralString, str, bytes]:
        """
        将音频文件转换为 WAV 格式。

        Args:
            audio_file_vo: 音频文件的值对象。

        Returns:
            转换后的音频文件路径。
        """
        return self.convert_for_fmt(audio_file_vo=audio_file_vo, format_flag='wav')

    def convert_for_fmt(self, audio_file_vo: FileVO, format_flag: str = 'mp3') -> Union[LiteralString, str, bytes]:
        """
        将音频文件转换为指定格式。

        Args:
            audio_file_vo: 音频文件的值对象。
            format_flag: 目标格式（如 'mp3'、'wav'）。

        Returns:
            转换后的音频文件路径。

        Raises:
            FileNotFoundError: 如果音频文件不存在。
            RuntimeError: 如果转换过程中发生错误。
        """
        self.log_info(f"开始将音频文件转换为 {format_flag} 格式：{audio_file_vo.file_path}")

        if not audio_file_vo.is_file:
            raise FileNotFoundError(f"音频文件 {audio_file_vo.file_path} 不存在")

        # 生成输出文件路径，避免覆盖原文件
        audio_output_path = os.path.join(
            audio_file_vo.file_dir,
            f"{audio_file_vo.file_only_name}1.{format_flag}"
        )

        try:
            # 转换音频文件，并设置采样率为 16k
            AudioTool.convert_audio(
                input_file_path=audio_file_vo.file_path,
                output_file_path=audio_output_path,
                format_flag=format_flag,
                sample_rate=16000
            )
        except Exception as e:
            raise RuntimeError(f"音频转换失败: {e}")

        self.log_info(f"结束将音频文件转换为 {format_flag} 格式")
        return audio_output_path
