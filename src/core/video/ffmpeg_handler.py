# coding: utf8
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Callable, Literal, Dict, Any

from core.base_object import BaseObject
from core.image.image_tool import ImageTool
from core.video.image_embed_arg import ImageEmbedArg
from model.file_vo import FileVO
from utils.uuid_utils import UuidUtils


class FfmpegHandler(BaseObject):
    """
    视频工具类，用 list 组织 ffmpeg 命令时，原命令中的双引号一般不需要，单引号需要保留，对于一些特殊格式，可能需要再参数前后分别加一个空格，
     如果文件路径中有空格，可能会导致不能正常执行命令，所以需要保证文件路径中没有空格。

    主要功能：
        1. 提取视频中的音频文件。
        2. 将字幕嵌入到视频文件中（支持硬字幕和软字幕）。
        3. 获取视频文件的详细信息。
    """

    def __init__(self, log_to_ui_func: Optional[Callable] = None):
        super().__init__(log_to_ui_func=log_to_ui_func)
        self.process = None

        # 注册退出处理
        import atexit
        atexit.register(self.stop)

    def _run_(self, cmd, title):
        self.log_info(f"正在{title}...，执行命令: {' '.join(cmd)}")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        error_msg = ""

        # 实时打印日志和错误输出
        while self.process.poll() is None:
            output = self.process.stdout.readline().strip()
            if output:
                # 解析进度百分比
                if "error" in output:
                    error_msg += output
                    self.log_error(output)
                else:
                    self.log_info(output)

        # 获取所有输出和错误信息
        self.process.communicate()

        self.log_info(f"{title}返回值: {self.process.returncode}")

        if error_msg:
            self.log_error(f"{title}错误: {error_msg}")
            raise RuntimeError(error_msg)

        return self.process.returncode

    def stop(self):
        """停止 ASR 语音识别处理。"""
        if self.process:
            self.log_info("终止 FFmpeg 进程")
            if os.name == 'nt':  # Windows系统
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:  # Linux/Mac系统
                import signal
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process = None

    def embed_1_image(self,
                      video_file_path: str,
                      out_video_path: str,
                      image_arg: ImageEmbedArg,
                      use_cuda: bool = False,
                      title: str = '把一个图片嵌入到视频'):
        """
        把一个图片嵌入到视频。

        Args:
            video_file_path: 视频文件。
            out_video_path: 输出视频文件。
            image_arg: 图片参数。
            use_cuda: 是否使用cuda。
            title: 这个功能的标题。
        """
        if not os.path.exists(image_arg.file_path):
            raise FileNotFoundError(f"图片文件 {image_arg.file_path} 不存在")

        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        complex_str = (f"[1]scale={image_arg.scale},format=rgba,"
                       f"colorchannelmixer=aa={image_arg.color_channel_mixer}[logo];"
                       f"[0][logo]overlay={image_arg.overlay_width}:{image_arg.overlay_height}"
                       f":enable='{image_arg.enable_time_period}'")

        cmd = ['ffmpeg']
        if use_cuda:
            cmd.extend(['-hwaccel', 'cuda'])
        cmd.extend([
            '-i', video_file_path,
            '-i', image_arg.file_path,
            '-filter_complex', complex_str,
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-y',
            out_video_path])

        if self._run_(cmd, title) == 0:
            return out_video_path
        else:
            return None

    def embed_2_image(self,
                      video_file_path: str,
                      out_video_path: str,
                      image_1_arg: ImageEmbedArg,
                      image_2_arg: ImageEmbedArg,
                      use_cuda: bool = False,
                      title: str = '把两个图片嵌入到视频'):
        """
        把两个图片嵌入到视频。

        Args:
            video_file_path: 视频文件。
            out_video_path: 输出视频文件。
            image_1_arg: 图片1参数。
            image_2_arg: 图片1参数。
            use_cuda: 是否使用cuda。
            title: 这个功能的标题。
        """
        if not os.path.exists(image_1_arg.file_path):
            raise FileNotFoundError(f"图片文件 {image_1_arg.file_path} 不存在")

        if not os.path.exists(image_2_arg.file_path):
            raise FileNotFoundError(f"图片文件 {image_2_arg.file_path} 不存在")

        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        complex_str = (f"[1:v]scale={image_1_arg.scale},format=rgba,"
                       f"colorchannelmixer=aa={image_1_arg.color_channel_mixer}[left_logo];"
                       f"[2:v]scale={image_2_arg.scale},format=rgba,"
                       f"colorchannelmixer=aa={image_2_arg.color_channel_mixer}[right_logo];"
                       f"[0:v][left_logo]overlay={image_1_arg.overlay_width}:{image_1_arg.overlay_height}"
                       f":enable='{image_1_arg.enable_time_period}'[tmp];"
                       f"[tmp][right_logo]overlay={image_2_arg.overlay_width}:{image_2_arg.overlay_height}"
                       f":enable='{image_2_arg.enable_time_period}'")
        cmd = ['ffmpeg']
        if use_cuda:
            cmd.extend(['-hwaccel', 'cuda'])
        cmd.extend([
            '-i', video_file_path,
            '-i', image_1_arg.file_path,
            '-i', image_2_arg.file_path,
            '-filter_complex', complex_str,
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-y',
            out_video_path])

        if self._run_(cmd, title) == 0:
            return out_video_path
        else:
            return None

    def image_to_mp4(self, image_file_path: str,
                     seconds: int = 2,
                     width: int = 1280,
                     height: int = 720,
                     frame_rate: int = 30,
                     use_cuda: bool = False,
                     audio_sampling_rate: int = 44100,
                     audio_channel_layout: str = 'mono',
                     title: str = '图片转视频'):
        """
        把图片转为mp4。

        Args:
            image_file_path: 图片文件。
            seconds: 视频时长。
            width(int): 宽。
            height(int): 宽。
            frame_rate: 帧率。
            use_cuda: 是否使用CUDA。
            audio_sampling_rate(int): 音频采样率。
            audio_channel_layout(str): 音频声道。
            title: 这个功能的标题。
        """
        scale: str = f"{width}:{height}"
        image_file_vo = FileVO(image_file_path)
        if not image_file_vo.is_file:
            raise FileNotFoundError(f"图片文件 {image_file_path} 不存在")

        if audio_sampling_rate <= 0:
            audio_sampling_rate = 44100

        output_dir = image_file_vo.file_dir
        out_img_file = os.path.join(output_dir, image_file_vo.file_only_name + '_tmp.' + image_file_vo.file_extension)
        try:
            ImageTool.resize_image(
                input_image_path=image_file_path,
                output_image_path=out_img_file,
                size=(width, height)
            )

            out_file_path = os.path.join(output_dir, image_file_vo.file_only_name + '.mp4')

            cmd = ['ffmpeg']
            if use_cuda:
                cmd.extend(['-hwaccel', 'cuda'])
            cmd.extend([
                '-loop', '1',
                '-i', out_img_file,
                '-f', 'lavfi',
                '-i', f'anullsrc=channel_layout={audio_channel_layout}:sample_rate={audio_sampling_rate}',
                '-c:v', 'libx264',
                '-t', f'{seconds}',
                '-pix_fmt', 'yuv420p',
                '-r', f'{frame_rate}',
                '-vf', f' scale={scale} ',  # 这里必须加前后空格
                '-shortest',
                '-c:a', 'aac',
                '-y', out_file_path])

            if self._run_(cmd, title) == 0:
                return out_file_path
            else:
                return None
        finally:
            if os.path.exists(out_img_file):
                os.remove(out_img_file)

    def concat_mp4(self, out_file_path: str,
                   concat_files: list[str],
                   video_codec: str = 'libx264',
                   preset: str = 'medium',
                   crf: int = 23,
                   scale: str = '1280:720',
                   frame_rate: int = 30,
                   bit_rate: str = '1M',
                   use_cuda: bool = False,
                   title: str = '拼接多个视频'):
        """
        拼接多个视频，把多个视频合并为一个视频。

        Args:
            out_file_path: 输出的视频文件路径。
            concat_files: 要合并的多个视频文件。
            video_codec: 视频编码。
            preset: 编码速度, 可用值包括 ultrafast, superfast, veryfast, faster, fast, medium（默认值）, slow, slower, veryslow。
            crf: 视频的恒定质量因子。
            scale: 分辨率。
            frame_rate: 帧率。
            bit_rate: 比特率。
            use_cuda: 是否使用CUDA。
            title: 这个功能的标题。
        """
        video_file_vo = FileVO(out_file_path)
        output_dir = video_file_vo.file_dir
        os.makedirs(output_dir, exist_ok=True)

        list_file = UuidUtils.generate_time_id() + '.txt'
        # list_file = os.path.join(output_dir, UuidUtils.generate_time_id() + '.txt')
        with open(list_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join([f"file '{filename}'" for filename in concat_files]))

        if os.path.exists(list_file):
            # ffmpeg -safe 0 -f concat -i file_list.txt -c:v libx264 -preset fast -crf 23 -c:a aac out1.mp4

            cmd = ['ffmpeg']
            # 2025-04-24，这里不用cuda，因为可能导致合并的视频失真，原因不详。
            # if use_cuda:
            #     cmd.extend(['-hwaccel', 'cuda'])
            cmd.extend([
                '-safe', '0',
                '-f', 'concat',
                '-i', list_file,
                '-c:v', video_codec,
                '-preset', preset,
                '-crf', f'{crf}',
                '-r', f'{frame_rate}',
                '-b:v', bit_rate,
                '-vf', f' scale={scale} ',
                '-c:a', 'aac',
                '-y',  # 覆盖输出文件
                out_file_path])
            try:
                if self._run_(cmd, title) == 0:
                    return out_file_path
                else:
                    return None
            finally:
                os.remove(list_file)
        return None

    def to_mp4(self,
               video_file_path: str,
               out_file_path: str,
               video_codec: str = 'libx264',
               preset: str = 'medium',
               crf: int = 23,
               scale: str = '1280:720',
               frame_rate: int = 30,
               bit_rate: str = '1M',
               use_cuda: bool = False,
               title: str = '视频重编码'):
        """
        把给定的视频文件转换为MP4。

        Args:
            out_file_path: 输出的视频文件路径。
            video_file_path: 要处理的视频文件。
            video_codec: 视频编码。
            preset: 编码速度, 可用值包括 ultrafast, superfast, veryfast, faster, fast, medium（默认值）, slow, slower, veryslow。
            crf: 视频的恒定质量因子。
            scale: 分辨率。
            frame_rate: 帧率。
            bit_rate: 比特率。
            use_cuda: 是否使用CUDA。
            title: 这个功能的标题。
        """
        video_file_vo = FileVO(out_file_path)
        output_dir = video_file_vo.file_dir
        os.makedirs(output_dir, exist_ok=True)

        cmd = ['ffmpeg']
        if use_cuda:
            cmd.extend(['-hwaccel', 'cuda'])
        cmd.extend([
            '-i', video_file_path,
            '-vf', f'scale={scale}',
            '-c:v', video_codec,
            '-crf', f'{crf}',
            '-preset', preset,
            '-b:v', bit_rate,
            '-r', f'{frame_rate}',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',  # 覆盖输出文件
            out_file_path])

        if self._run_(cmd, title) == 0:
            return out_file_path
        else:
            return None

    def extract_audio(self,
                      video_file_path: str,
                      out_file_path: str,
                      audio_channel_idx: int = 0,  # 音频流序号
                      audio_channel_num: int = 1,  # 音频通道数量，1 将音频转换为单声道（Mono）；2 将音频转换为双声道；6 转换为5.1环绕声。
                      audio_rate: str = '16000',  # 采样率
                      title: str = '从视频文件中提取音频'):
        """
        使用 FFmpeg 从视频文件中提取音频。

        Args:
            video_file_path: 视频文件路径。
            out_file_path: 输出文件路径。
            audio_channel_idx(int): 音频流序号。
            audio_channel_num(int): 音频通道数量，1 将音频转换为单声道（Mono）；2 将音频转换为双声道；6 转换为5.1环绕声。
            audio_rate(str): 采样率。
            title: 这个功能的标题。

        Returns:
            提取的音频文件路径。

        Raises:
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        cmd = [
            'ffmpeg',
            '-i', video_file_path,
            '-map', f'0:a:{audio_channel_idx}',
            '-ac', f'{audio_channel_num}',
            '-ar', f'{audio_rate}',  # 16K 采样率
            '-af', 'aresample=async=1',  # 处理音频同步问题
            '-y',  # 覆盖输出文件
            out_file_path
        ]
        if self._run_(cmd, title) == 0:
            return out_file_path
        else:
            return None

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

    def add_hard_subtitles(self, video_file_path: str, subtitle_file: str, out_file_path: str,
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
            out_file_path: 输出文件路径。
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

        out_vo = FileVO(out_file_path)
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
            out_file_path
        ])

        self.log_info(f"添加硬字幕执行命令: {' '.join(cmd)}")
        return self._run_add_subtitles_(cmd, "视频合成")

    def add_soft_subtitles(self, video_file_path: str, subtitle_file: str, out_file_path: str) -> str:
        """
        使用软字幕将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            subtitle_file: 字幕文件路径。
            out_file_path: 输出文件路径。

        Returns:
            嵌入字幕后的视频文件路径。

        Raises:
            RuntimeError: 如果字幕嵌入失败。
        """
        self.log_info("使用软字幕合成")
        cmd = [
            'ffmpeg',
            '-i', video_file_path,
            '-i', subtitle_file,
            '-c:v', 'copy',  # 拷贝视频
            '-c:a', 'copy',  # 拷贝音频
            '-c:s', 'mov_text',  # 字幕编码
            '-y',  # 覆盖输出文件
            out_file_path
        ]
        self.log_info(f"添加软字幕执行命令: {' '.join(cmd)}")
        return self._run_add_subtitles_(cmd, "视频合成")

    def _run_add_subtitles_(self, cmd: list, task_name: str) -> str:
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
            'audio_channel_layout': '',
            'audio_sampling_rate': 0,
            'thumbnail_path': '',
        }

        try:
            # 构建ffmpeg命令
            cmd = ["ffmpeg", "-i", file_path]
            self.log_info(f"获取视频信息执行命令: {' '.join(cmd)}")

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
            audio_info = self._extract_audio_info_(info)
            if audio_info:
                video_info.update({
                    'audio_codec': audio_info['codec'],
                    'audio_channel_layout': audio_info['channel_layout'],
                    'audio_sampling_rate': int(audio_info['sample_rate'])
                })

            return video_info

        except Exception as e:
            # 记录异常信息并返回初始化的视频信息
            self.log_exception(f"获取视频信息时出错: {str(e)}")
            return {k: '' if isinstance(v, str) else 0 for k, v in video_info.items()}

    @staticmethod
    def _extract_audio_info_(ffmpeg_line):
        """
        从 FFmpeg 的流信息中提取音频元数据
        示例输入：
        'Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 48 kb/s (default)'

        返回字典格式：
        {
            'codec': 'aac',
            'profile': 'LC',
            'codec_tag': 'mp4a',
            'sample_rate': 44100,
            'channels': 'mono',
            'channel_layout': 'mono',
            'sample_format': 'fltp',
            'bitrate': 48,
            'bitrate_unit': 'kb/s',
            'default': True
        }
        """
        pattern = re.compile(
            r"Stream.*Audio: (\w+) \((\w+)\) \((\w+).*\)?, (\d+) Hz, (\w+), (\w+), (\d+) (kb/s|mb/s)(?: \(default\))?"
        )
        match = pattern.search(ffmpeg_line)

        if not match:
            # 尝试匹配无 profile 的情况（如 mp3）
            pattern_fallback = re.compile(
                r"Stream.*Audio: (\w+).*?, (\d+) Hz, (\w+), (\w+), (\d+) (kb/s|mb/s)(?: \(default\))?"
            )
            match = pattern_fallback.search(ffmpeg_line)
            if not match:
                return None

        groups = match.groups()

        info = {
            'codec': groups[0],
            'profile': groups[1] if len(groups) >= 8 else None,
            'codec_tag': groups[2] if len(groups) >= 8 else None,
            'sample_rate': int(groups[-5] if len(groups) >= 8 else groups[1]),
            'channels': groups[-4] if len(groups) >= 8 else groups[2],
            'channel_layout': groups[-4] if len(groups) >= 8 else groups[2],
            'sample_format': groups[-3] if len(groups) >= 8 else groups[3],
            'bitrate': int(groups[-2]),
            'bitrate_unit': groups[-1],
            'default': '(default)' in ffmpeg_line
        }

        return info