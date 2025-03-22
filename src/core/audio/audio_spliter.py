# coding: utf8
from pydub import AudioSegment
import os
import math

from utils.common_utils import print_progress_bar
from model.file_vo import FileVO


class AudioSpliter:
    """音频分割工具类，用于将音频文件分割为多个小文件或拆分为左右声道。"""

    @staticmethod
    def split_mp3(input_file: str, output_folder: str, output_prefix: str, chunk_duration_seconds: int = 100) -> None:
        """将一个大的 MP3 文件按照指定时长拆分为多个小文件。

        Args:
            input_file (str): 要处理的 MP3 文件路径。
            output_folder (str): 拆分后的文件输出目录。
            output_prefix (str): 输出文件名的前缀，完整的文件名是 {output_prefix}{index+1}.mp3。
            chunk_duration_seconds (int, optional): 拆分音频时长（秒），默认是 100 秒。
        """
        AudioSpliter.split_audio(
            input_file=input_file,
            output_folder=output_folder,
            output_prefix=output_prefix,
            chunk_duration_seconds=chunk_duration_seconds
        )

    @staticmethod
    def split_wav(input_file: str, output_folder: str, output_prefix: str, chunk_duration_seconds: int = 100) -> None:
        """将一个大的 WAV 文件按照指定时长拆分为多个小文件。

        Args:
            input_file (str): 要处理的 WAV 文件路径。
            output_folder (str): 拆分后的文件输出目录。
            output_prefix (str): 输出文件名的前缀，完整的文件名是 {output_prefix}{index+1}.wav。
            chunk_duration_seconds (int, optional): 拆分音频时长（秒），默认是 100 秒。
        """
        AudioSpliter.split_audio(
            input_file=input_file,
            output_folder=output_folder,
            output_prefix=output_prefix,
            output_format='wav',
            chunk_duration_seconds=chunk_duration_seconds
        )

    @staticmethod
    def split_audio(input_file: str, output_folder: str, output_prefix: str,
                    output_format: str = 'mp3', chunk_duration_seconds: int = 100) -> None:
        """将一个大的音频文件按照指定时长拆分为多个小文件。

        Args:
            input_file (str): 要处理的音频文件路径。
            output_folder (str): 拆分后的文件输出目录。
            output_prefix (str): 输出文件名的前缀，完整的文件名是 {output_prefix}{index+1}.{output_format}。
            output_format (str, optional): 输出文件格式，默认为 'mp3'。
            chunk_duration_seconds (int, optional): 拆分音频时长（秒），默认是 100 秒。

        Raises:
            FileNotFoundError: 如果输入文件不存在。
        """
        chunk_duration_ms = chunk_duration_seconds * 1000

        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"文件 {input_file} 不存在")

        # 确保输出文件夹存在
        os.makedirs(output_folder, exist_ok=True)

        print(f'加载 {input_file}')
        file_vo = FileVO(input_file)
        if file_vo.file_extension == 'mp3':
            audio = AudioSegment.from_mp3(input_file)  # 加载 MP3 文件
        else:
            audio = AudioSegment.from_wav(input_file)  # 加载 WAV 文件

        total_duration_ms = len(audio)  # 获取音频的总持续时间（毫秒）
        chunk_index = 0  # 初始化计数器
        total_steps = math.ceil(total_duration_ms / chunk_duration_ms)  # 总步数

        print(f'分割 {input_file}，共 {total_steps} 个片段')
        start_time = 0
        while start_time < total_duration_ms:
            end_time = min(start_time + chunk_duration_ms, total_duration_ms)  # 计算结束时间
            chunk = audio[start_time:end_time]  # 提取当前块的音频

            # 构造输出文件名
            output_file = os.path.join(output_folder, f"{output_prefix}{10000 + chunk_index}.{output_format}")

            # 导出当前块的音频
            chunk.export(output_file, format=output_format, bitrate='16k')

            chunk_index += 1  # 更新计数器
            start_time = end_time  # 更新开始时间为下一个块的开始时间

            # 打印进度条
            print_progress_bar(chunk_index, total_steps, prefix=output_prefix + ':', suffix='完成')

    @staticmethod
    def split_stereo_to_mono(audio_path: str, left_output_path: str, right_output_path: str) -> None:
        """将立体声音频文件拆分为左右声道，并保存为两个单声道文件。

        Args:
            audio_path (str): 要处理的音频文件路径。
            left_output_path (str): 左声道输出的文件路径。
            right_output_path (str): 右声道输出的文件路径。

        Raises:
            FileNotFoundError: 如果输入文件不存在。
        """
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"音频文件 {audio_path} 不存在")

        audio = AudioSegment.from_file(audio_path)  # 加载音频文件
        left_channel = audio.split_to_mono()[0]  # 提取左声道
        right_channel = audio.split_to_mono()[1]  # 提取右声道

        # 导出左右声道为 WAV 文件
        left_channel.export(left_output_path, format="wav")
        right_channel.export(right_output_path, format="wav")
