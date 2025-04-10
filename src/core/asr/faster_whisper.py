# coding: utf8
import os
import re
import shutil
import subprocess
from pathlib import Path
import tempfile
from typing import List

from enums.faster_whisper_enums import FasterWhisperDeviceEnum
from .asr_data_seg import ASRDataSeg
from .asr_data_builder import AsrDataBuilder
from .base_asr import BaseASR


class FasterWhisper(BaseASR):
    """FasterWhisper 类，用于实现基于 Faster Whisper 的语音识别功能。

    Attributes:
        model_path (str): Whisper 模型路径。
        model_dir (str): 模型目录。
        faster_whisper_path (Path): Faster Whisper 可执行文件路径。
        need_word_time_stamp (bool): 是否需要单词级别的时间戳。
        language (str): 识别语言，默认为中文。
        device (str): 使用的设备，默认为 CPU。
        output_dir (str): 输出目录。
        output_format (str): 输出格式，默认为 SRT。
        vad_filter (bool): 是否启用 VAD 过滤。
        vad_threshold (float): VAD 阈值。
        vad_method (str): VAD 方法。
        ff_mdx_kim2 (bool): 是否启用 FF MDX Kim2 音频处理。
        one_word (int): 是否启用单字模式。
        sentence (bool): 是否启用句子模式。
        max_line_width (int): 最大行宽。
        max_line_count (int): 最大行数。
        max_comma (int): 最大逗号数。
        max_comma_cent (int): 最大逗号百分比。
        process (subprocess.Popen): 子进程对象。
    """

    def __init__(self,
                 audio_path: str,
                 faster_whisper_path: str,
                 whisper_model: str,
                 model_dir: str,
                 language: str = "zh",
                 device: str = "auto",
                 use_cache: bool = False,
                 output_dir: str = None,
                 output_format: str = "srt",
                 need_word_time_stamp: bool = False,
                 vad_filter: bool = True,
                 vad_threshold: float = 0.4,
                 vad_method: str = "silero_v4",
                 ff_mdx_kim2: bool = False,
                 one_word: int = 0,
                 sentence: bool = False,
                 prompt: str = "",
                 max_line_width: int = 100,
                 max_line_count: int = 1,
                 max_comma: int = 20,
                 max_comma_cent: int = 50,
                 log_to_ui_func=None):
        """初始化 FasterWhisper 实例。

        Args:
            audio_path (str): 音频文件路径。
            faster_whisper_path (str): Faster Whisper 可执行文件路径。
            whisper_model (str): Whisper 模型路径。
            model_dir (str): 模型目录。
            language (str, optional): 识别语言，默认为中文。
            device (str, optional): 使用的设备，默认为 auto, 自动检测。
            use_cache (bool, optional): 是否使用缓存。
            output_dir (str, optional): 输出目录。
            output_format (str, optional): 输出格式，默认为 SRT。
            need_word_time_stamp (bool, optional): 是否需要单词级别的时间戳。
            vad_filter (bool, optional): 是否启用 VAD 过滤。
            vad_threshold (float, optional): VAD 阈值。
            vad_method (str, optional): VAD 方法。
            ff_mdx_kim2 (bool, optional): 是否启用 FF MDX Kim2 音频处理。
            one_word (int, optional): 是否启用单字模式。
            sentence (bool, optional): 是否启用句子模式。
            max_line_width (int, optional): 最大行宽。
            max_line_count (int, optional): 最大行数。
            max_comma (int, optional): 最大逗号数。
            max_comma_cent (int, optional): 最大逗号百分比。
            log_to_ui_func (function, optional): 日志输出函数。
        """
        super().__init__(audio_path=audio_path, use_cache=False, log_to_ui_func=log_to_ui_func)

        # 基本参数
        self.model_path = whisper_model
        self.model_dir = model_dir
        self.faster_whisper_path = Path(faster_whisper_path)
        self.need_word_time_stamp = need_word_time_stamp
        self.language = language
        self.device = device
        self.use_cache = use_cache
        self.output_dir = output_dir
        self.output_format = output_format

        # VAD 参数
        self.vad_filter = vad_filter
        self.vad_threshold = vad_threshold
        self.vad_method = vad_method

        # 音频处理参数
        self.ff_mdx_kim2 = ff_mdx_kim2

        # 文本处理参数
        self.one_word = one_word
        self.sentence = sentence
        self.prompt = prompt
        self.max_line_width = max_line_width
        self.max_line_count = max_line_count
        self.max_comma = max_comma
        self.max_comma_cent = max_comma_cent

        self.process = None

        # 注册退出处理
        import atexit
        atexit.register(self.stop)

    def _build_command(self, audio_path: Path) -> List[str]:
        """构建命令行参数。

        Args:
            audio_path (Path): 音频文件路径。

        Returns:
            List[str]: 命令行参数列表。
        """
        cmd = [
            str(self.faster_whisper_path),
            "-m", str(self.model_path),
            "--print_progress"
        ]

        # 添加模型目录参数
        if self.model_dir:
            cmd.extend(["--model_dir", str(self.model_dir)])

        # 基本参数
        cmd.extend([
            str(audio_path),
            "--output_format", self.output_format,
        ])

        if self.device != FasterWhisperDeviceEnum.AUTO.value:
            cmd.extend(["-d", self.device])

        if self.language:
            cmd.extend(["-l", self.language])

        # 输出目录
        if self.output_dir:
            cmd.extend(["-o", str(self.output_dir)])
        else:
            cmd.extend(["-o", "source"])

        # VAD 相关参数
        if self.vad_filter:
            cmd.extend([
                "--vad_filter", "true",
                "--vad_threshold", f"{self.vad_threshold:.2f}",
            ])
            if self.vad_method:
                cmd.extend(["--vad_method", self.vad_method])

        # 人声分离
        if self.ff_mdx_kim2:
            cmd.append("--ff_mdx_kim2")

        # 文本处理参数
        if self.one_word:
            self.one_word = 1
        else:
            self.one_word = 0
        if self.one_word in [0, 1, 2]:
            cmd.extend(["--one_word", str(self.one_word)])

        if self.sentence:
            cmd.extend([
                "--sentence",
                "--max_line_width", str(self.max_line_width),
                "--max_line_count", str(self.max_line_count),
                "--max_comma", str(self.max_comma),
                "--max_comma_cent", str(self.max_comma_cent)
            ])

        return cmd

    def _make_segments(self, resp_data: str) -> list[ASRDataSeg]:
        """生成 ASR 数据段。

        Args:
            resp_data (str): 响应数据。

        Returns:
            list[ASRDataSeg]: ASR 数据段列表。
        """
        asr_data = AsrDataBuilder.from_srt(resp_data)
        # 过滤掉纯音乐标记
        filtered_segments = []
        for seg in asr_data.segments:
            text = seg.text.strip()
            if not (text.startswith('【') or
                    text.startswith('[') or
                    text.startswith('(') or
                    text.startswith('（')):
                filtered_segments.append(seg)
        return filtered_segments

    def _run(self, callback=None, **kwargs) -> str:
        """运行 Faster Whisper 语音识别。

        Args:
            callback (function, optional): 回调函数。
            **kwargs: 其他参数。

        Returns:
            str: 识别结果。

        Raises:
            RuntimeError: 如果识别失败。
        """
        temp_dir = Path(tempfile.gettempdir()) / "bk_asr"
        temp_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(dir=temp_dir) as temp_path:
            temp_dir = Path(temp_path)
            wav_path = temp_dir / "music.wav"
            output_path = wav_path.with_suffix(".srt")

            shutil.copy2(self.audio_path, wav_path)

            cmd = self._build_command(wav_path)

            self.log_info(f"Faster Whisper 执行命令: {' '.join(cmd)}")

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            is_finish = False
            error_msg = ""

            # 实时打印日志和错误输出
            pre_pregress = 0
            while self.process.poll() is None:
                output = self.process.stdout.readline().strip()
                if output:
                    # 解析进度百分比
                    if "error" in output:
                        error_msg += output
                        self.log_error(output)
                    elif match := re.search(r'(\d+)%', output):
                        progress = int(match.group(1))
                        if progress >= 95:
                            is_finish = True
                        if pre_pregress != progress:
                            if output.startswith("MDX"):
                                self.log_info(f"消除背景乐，{output}")
                            else:
                                self.log_info(output)
                        pre_pregress = progress
                    else:
                        self.log_info(output)

            # 获取所有输出和错误信息
            self.process.communicate()

            self.log_info(f"Faster Whisper 返回值: {self.process.returncode}")
            if not is_finish:
                self.log_error(f"Faster Whisper 错误: {error_msg}")
                raise RuntimeError(error_msg)

            # 判断是否识别成功
            if not output_path.exists():
                raise RuntimeError(f"Faster Whisper 输出文件不存在: {output_path}")

            self.log_info("Faster Whisper 识别完成")

            return output_path.read_text(encoding='utf-8')

    def _get_key(self):
        """获取缓存键值。

        Returns:
            str: 缓存键值。
        """
        return (f"{self.__class__.__name__}-{self.crc32_hex}-"
                f"{self.need_word_time_stamp}-{self.model_path}-{self.language}")

    def stop(self):
        """停止 ASR 语音识别处理。"""
        if self.process:
            self.log_info("终止 Faster Whisper ASR 进程")
            if os.name == 'nt':  # Windows系统
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:  # Linux/Mac系统
                import signal
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process = None
