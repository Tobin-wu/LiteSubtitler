# coding: utf8
import os
import re
import subprocess
from pydub import AudioSegment
import wave


class AudioTool:
    """音频处理工具类，提供人声增强和音频格式转换功能。"""

    @staticmethod
    def read_wav_duration(file_path: str) -> float:
        """
        读取 WAV 文件的时长（以秒为单位）。

        Args:
            file_path: WAV 文件的路径。

        Returns:
            WAV 文件的时长（秒）。

        Raises:
            FileNotFoundError: 如果文件不存在。
            RuntimeError: 如果读取过程中发生错误。
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        try:
            with wave.open(file_path, "r") as wav_file:
                frame_count = wav_file.getnframes()  # 获取帧数
                frame_rate = wav_file.getframerate()  # 获取采样率
                return frame_count / frame_rate  # 计算时长
        except Exception as e:
            raise RuntimeError(f"读取 WAV 文件时长失败: {e}")

    @staticmethod
    def enhance_human(filepath: str, out_file_path: str) -> bool:
        """对音频文件进行人声增强处理。

        使用 FFmpeg 的 equalizer 滤波器增强人声频段（300Hz、1000Hz、3000Hz）。

        Args:
            filepath (str): 输入音频文件路径。
            out_file_path (str): 输出音频文件路径。

        Returns:
            bool: 处理是否成功。如果 FFmpeg 输出中包含成功标志，则返回 True，否则返回 False。

        Example:
            >>> AudioTool.enhance_human("input.wav", "output.wav")
            True
        """
        # 定义 FFmpeg 的 equalizer 滤波器参数
        arg_300 = "equalizer=f=300:width_type=o:width=2:g=5"
        arg_1000 = "equalizer=f=1000:width_type=o:width=2:g=5"
        arg_3000 = "equalizer=f=3000:width_type=o:width=2:g=5"

        # 构建 FFmpeg 命令
        cmd = [
            "ffmpeg",
            "-i", filepath,
            "-af", f"{arg_300}, {arg_1000}, {arg_3000}",
            "-y",  # 覆盖输出文件
            out_file_path
        ]

        print(f"enhance_human 执行命令: {' '.join(cmd)}")

        # 执行 FFmpeg 命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )

        # 打印 FFmpeg 输出信息
        info = result.stderr
        print(info)

        # 使用正则表达式检查 FFmpeg 输出是否包含成功标志
        success_pattern = re.compile(r"size=\s*\d+KiB\s+time=\d{2}:\d{2}:\d{2}\.\d{2}\s+bitrate=\s*\d+\.\d+kbits/s")
        return bool(success_pattern.search(info))

    @staticmethod
    def convert_audio(input_file_path: str, output_file_path: str, format_flag: str = None,
                      bit_rate: str = None, sample_rate: int = 44100) -> None:
        """将音频文件转换为指定格式。

        支持通过参数指定输出格式、比特率和采样率。

        Args:
            input_file_path (str): 输入音频文件路径。
            output_file_path (str): 输出音频文件路径（包含目标格式扩展名）。
            format_flag (str, optional): 目标格式（如 'mp3', 'wav'）。如果为 None，则从输出文件扩展名推断。
            bit_rate (str, optional): 目标比特率（如 '128k', '192k'）。如果为 None，则使用默认值。
            sample_rate (int, optional): 目标采样率，默认为 44100Hz。

        Example:
            >>> AudioTool.convert_audio("input.wav", "output.mp3", format_flag="mp3", bit_rate="192k")
        """
        # 加载音频文件
        audio = AudioSegment.from_file(input_file_path)

        # 导出音频文件到目标格式
        if format_flag:
            audio.export(
                output_file_path,
                format=format_flag,
                bitrate=bit_rate,
                parameters=["-ar", str(sample_rate)]  # 设置采样率
            )
        else:
            # 如果未指定格式，则从输出文件扩展名推断
            audio.export(output_file_path)
