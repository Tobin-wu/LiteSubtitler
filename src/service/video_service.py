# coding: utf8
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Literal, Optional, Dict, Callable, Any

from core.asr.asr_data import ASRData
from core.base_object import BaseObject
from model.file_vo import FileVO
from utils.dict_utils import DictUtils


class VideoService(BaseObject):
    """
    视频服务类，用于处理视频文件的音频提取、字幕嵌入和视频信息获取。

    主要功能：
        1. 提取视频中的音频文件。
        2. 将字幕嵌入到视频文件中（支持硬字幕和软字幕）。
        3. 获取视频文件的详细信息。
    """

    def __init__(self, log_to_ui_func: Optional[Callable] = None):
        """
        初始化视频服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self._args = {
            "subtitle_layout": "译文在上",  # 字幕布局
            "quality": 'medium',
            # 压制方式，支持 ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
            "is_embed_subtitle": False,  # 是否将字幕嵌入视频
            "is_soft_subtitle": False,  # 是否使用软字幕
            "style_str": (
                "[V4+ Styles]\n"
                "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,"
                "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
                "Alignment,MarginL,MarginR,MarginV,Encoding\n"
                "Style: Default,MicrosoftYaHei-Bold,40,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1\n"
                "Style: Secondary,MicrosoftYaHei-Bold,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1"
            )  # ASS 字幕样式
        }

    def reset_args(self, the_args: Dict[str, Any]) -> None:
        """
        重置视频处理参数。

        Args:
            the_args: 包含新参数的字典。
        """
        DictUtils.update_by_key(self._args, the_args)

        if 'default_style' in the_args and 'secondary_style' in the_args:
            self._args["style_str"] = ASRData.read_ass_style(the_args)

    def extract_mp3(self, video_file_path: str) -> str:
        """
        从视频文件中提取 MP3 音频。

        Args:
            video_file_path: 视频文件路径。

        Returns:
            提取的 MP3 文件路径。

        Raises:
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        return self._extract_audio(video_file_path, codec='libmp3lame', ext_name='mp3')

    def extract_wav(self, video_file_path: str, codec: str = 'pcm_s16le') -> str:
        """
        从视频文件中提取 WAV 音频。

        Args:
            video_file_path: 视频文件路径。
            codec: 音频编码格式，支持 ['pcm_s16le', 'pcm_s24le', 'pcm_s32le']。

        Returns:
            提取的 WAV 文件路径。

        Raises:
            ValueError: 如果 codec 不支持。
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        if codec not in ['pcm_s16le', 'pcm_s24le', 'pcm_s32le']:
            raise ValueError(f"不支持的 codec 值: {codec}")
        return self._extract_audio(video_file_path, codec=codec, ext_name='wav')

    def _extract_audio(self, video_file_path: str, codec: str, ext_name: str) -> str:
        """
        使用 FFmpeg 从视频文件中提取音频。

        Args:
            video_file_path: 视频文件路径。
            codec: 音频编码格式。
            ext_name: 输出文件扩展名。

        Returns:
            提取的音频文件路径。

        Raises:
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        video_file_vo = FileVO(video_file_path)
        if not video_file_vo.is_file:
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        output_dir = video_file_vo.file_dir
        os.makedirs(output_dir, exist_ok=True)

        output = os.path.join(output_dir, f"{video_file_vo.file_only_name}.{ext_name}")
        cmd = [
            'ffmpeg',
            '-i', video_file_path,
            '-map', '0:a:0',  # 第一个音频流
            '-ac', '1',  # 单声道
            '-ar', '16000',  # 16K 采样率
            '-af', 'aresample=async=1',  # 处理音频同步问题
            '-y',  # 覆盖输出文件
            output
        ]
        self.log_info(f"正在提取音频流...，执行命令: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
            )
            if result.returncode == 0 and os.path.exists(output):
                return output
            else:
                raise RuntimeError(f"音频转换失败: {result.stderr}")
        except Exception as e:
            self.log_exception(f"音频转换出错: {str(e)}")
            raise RuntimeError(f"音频转换出错: {e}")

    def embed_subtitles(self, video_file_path: str, asr_data: ASRData, vcodec: str = 'libx264') -> ASRData:
        """
        将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            asr_data: 包含字幕数据的 ASRData 对象。
            vcodec: 视频编码格式。

        Returns:
            处理后的 ASRData 对象。

        Raises:
            RuntimeError: 如果视频文件不存在或字幕嵌入失败。
        """
        if not self._args['is_embed_subtitle']:
            self.log_warning("无需合成，系统配置为‘不把字幕合成到视频’")
            return asr_data

        self.log_info("开始: 嵌入字幕到视频文件")

        video_file_vo = FileVO(video_file_path)
        if not video_file_vo.is_file:
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        temp_dir = os.path.join(video_file_vo.file_dir, "out")
        os.makedirs(temp_dir, exist_ok=True)

        temp_subtitle = os.path.join(temp_dir, f"temp_{int(time.time())}.ass")
        try:
            asr_data.to_ass(style_str=self._args['style_str'],
                            layout=self._args['subtitle_layout'],
                            save_path=temp_subtitle)
            if os.path.exists(temp_subtitle):
                output = os.path.join(temp_dir, f"【LS】{video_file_vo.file_only_name}.{video_file_vo.file_extension}")
                if self._args['is_soft_subtitle']:
                    self._add_soft_subtitles(video_file_path, temp_subtitle, output)
                else:
                    self._add_hard_subtitles(video_file_path, temp_subtitle, output, self._args['quality'], vcodec)
                self.log_info(f"嵌入字幕的视频文件：{output}")
            else:
                self.log_warning(f"待嵌入的字幕不存在：{temp_subtitle}")
            return asr_data
        finally:
            if os.path.exists(temp_subtitle):
                os.remove(temp_subtitle)
            self.log_info("完成：嵌入字幕到视频文件。")

    def _add_hard_subtitles(self, video_file_path: str, subtitle_file: str, output: str,
                            quality: Literal[
                                'ultrafast', 'superfast', 'veryfast', 'faster', 'fast',
                                'medium', 'slow', 'slower', 'veryslow'
                            ],
                            vcodec: str) -> str:
        """
        使用硬字幕将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            subtitle_file: 字幕文件路径。
            output: 输出文件路径。
            quality: 压制质量。
            vcodec: 视频编码格式。

        Returns:
            嵌入字幕后的视频文件路径。

        Raises:
            RuntimeError: 如果字幕嵌入失败。
        """
        self.log_info("使用硬字幕")
        subtitle_file = Path(subtitle_file).as_posix().replace(':', r'\:')
        vf = f"subtitles='{subtitle_file}'"

        out_vo = FileVO(output)
        if out_vo.file_extension == 'webm':
            vcodec = 'libvpx-vp9'
            self.log_info("WebM 格式视频，使用 libvpx-vp9 编码器")

        use_cuda = self.check_cuda_available()
        cmd = ['ffmpeg']
        if use_cuda:
            self.log_info("使用 CUDA 加速")
            cmd.extend(['-hwaccel', 'cuda'])
        cmd.extend([
            '-i', video_file_path,
            '-acodec', 'copy',  # 拷贝音频
            '-vcodec', vcodec,  # 视频编码
            '-preset', quality,  # 压制方式
            '-vf', f' {vf} ',  # 字幕
            '-y',  # 覆盖输出文件
            output
        ])

        self.log_info(f"添加硬字幕执行命令: {' '.join(cmd)}")
        return self._run_ffmpeg_command(cmd, "视频合成")

    def _add_soft_subtitles(self, video_file_path: str, subtitle_file: str, output: str) -> str:
        """
        使用软字幕将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            subtitle_file: 字幕文件路径。
            output: 输出文件路径。

        Returns:
            嵌入字幕后的视频文件路径。

        Raises:
            RuntimeError: 如果字幕嵌入失败。
        """
        self.log_info("使用软字幕")
        cmd = [
            'ffmpeg',
            '-i', video_file_path,
            '-i', subtitle_file,
            '-c:v', 'copy',  # 拷贝视频
            '-c:a', 'copy',  # 拷贝音频
            '-c:s', 'mov_text',  # 字幕编码
            output,
            '-y'  # 覆盖输出文件
        ]
        self.log_info(f"添加软字幕执行命令: {' '.join(cmd)}")
        return self._run_ffmpeg_command(cmd, "视频合成")

    def _run_ffmpeg_command(self, cmd: list, task_name: str) -> str:
        """
        执行 FFmpeg 命令并处理输出。

        Args:
            cmd: FFmpeg 命令列表。
            task_name: 任务名称，用于日志记录。

        Returns:
            输出文件路径。

        Raises:
            RuntimeError: 如果命令执行失败。
        """
        process = None
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
            )

            total_duration = None
            current_time = 0
            pre_progress = -1

            while True:
                output_line = process.stderr.readline()
                if not output_line or (process.poll() is not None):
                    break

                if total_duration is None:
                    duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})', output_line)
                    if duration_match:
                        h, m, s = map(float, duration_match.groups())
                        total_duration = h * 3600 + m * 60 + s
                        self.log_info(f"视频总时长: {total_duration}秒")

                time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2}\.\d{2})', output_line)
                if time_match:
                    h, m, s = map(float, time_match.groups())
                    current_time = h * 3600 + m * 60 + s

                if total_duration:
                    progress = round((current_time / total_duration) * 100)
                    if pre_progress != progress:
                        self.log_info(f"{progress}% : 正在合成")
                        pre_progress = progress

            return_code = process.wait()
            if return_code != 0:
                error_info = process.stderr.read()
                raise RuntimeError(f"{task_name}失败: {error_info}")
            self.log_info(f"{task_name}完成")
            return cmd[-1]  # 返回输出文件路径
        except Exception as e:
            self.log_error(f"{task_name}出错: {str(e)}")
            raise
        finally:
            if process and process.poll() is None:
                process.kill()

    def check_cuda_available(self) -> bool:
        """
        检查 CUDA 是否可用。

        Returns:
            CUDA 是否可用。
        """
        self.log_info("检查 CUDA 是否可用")
        try:
            result = subprocess.run(
                ['ffmpeg', '-hwaccels'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
            )
            if 'cuda' not in result.stdout.lower():
                self.log_info("CUDA 不在支持的硬件加速器列表中")
                return False

            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-init_hw_device', 'cuda'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if any(error in result.stderr.lower() for error in ['cannot load cuda', 'failed to load', 'error']):
                self.log_info("CUDA 设备初始化失败")
                return False
            self.log_info("CUDA 可用")
            return True
        except Exception as e:
            self.log_error(f"检查 CUDA 出错: {str(e)}")
            return False

    def get_video_info(self, file_path: str) -> Dict[str, Any]:
        """获取视频文件的详细信息。

        Args:
            file_path (str): 视频文件的路径。

        Returns:
            Dict[str, Any]: 包含视频信息的字典。如果发生错误，返回的字典中所有值将被初始化为空字符串或0。
        """
        # 初始化视频信息字典
        video_info = {
            'file_name': Path(file_path).stem,
            'duration_seconds': 0,
            'bitrate_kbps': 0,
            'video_codec': '',
            'width': 0,
            'height': 0,
            'fps': 0,
            'audio_codec': '',
            'audio_sampling_rate': 0,
            'thumbnail_path': '',
        }

        try:
            # 构建ffmpeg命令
            cmd = ["ffmpeg", "-i", file_path]
            self.logger.info(f"获取视频信息执行命令: {' '.join(cmd)}")

            # 执行ffmpeg命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )

            # 获取ffmpeg输出信息
            info = result.stderr

            # 提取视频时长
            if duration_match := re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', info):
                hours, minutes, seconds = map(float, duration_match.groups())
                video_info['duration_seconds'] = hours * 3600 + minutes * 60 + seconds
                self.log_info(f"视频时长: {video_info['duration_seconds']}秒")

            # 提取比特率
            if bitrate_match := re.search(r'bitrate: (\d+) kb/s', info):
                video_info['bitrate_kbps'] = int(bitrate_match.group(1))

            # 提取视频流信息
            if video_stream_match := re.search(
                    r'Stream #\d+:\d+.*Video: (\w+).*?, (\d+)x(\d+).*?, ([\d.]+) (?:fps|tb)',
                    info, re.DOTALL
            ):
                video_info.update({
                    'video_codec': video_stream_match.group(1),
                    'width': int(video_stream_match.group(2)),
                    'height': int(video_stream_match.group(3)),
                    'fps': float(video_stream_match.group(4))
                })

            # 提取音频流信息
            if audio_stream_match := re.search(
                    r'Stream #\d+:\d+.*Audio: (\w+).* (\d+) Hz', info
            ):
                video_info.update({
                    'audio_codec': audio_stream_match.group(1),
                    'audio_sampling_rate': int(audio_stream_match.group(2))
                })

            return video_info

        except Exception as e:
            # 记录异常信息并返回初始化的视频信息
            self.log_exception(f"获取视频信息时出错: {str(e)}")
            return {k: '' if isinstance(v, str) else 0 for k, v in video_info.items()}
