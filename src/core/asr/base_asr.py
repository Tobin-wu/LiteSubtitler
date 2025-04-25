# coding: utf8
import json
import os
import threading
import zlib
from typing import Optional, Union

from config import CACHE_PATH
from core.base_object import BaseObject
from .asr_data import ASRData
from .asr_data_seg import ASRDataSeg


class BaseASR(BaseObject):
    """ASR 基类，提供音频识别的基本功能和缓存管理。

    Attributes:
        SUPPORTED_SOUND_FORMAT (list): 支持的音频格式。
        CACHE_FILE (str): 缓存文件路径。
        _lock (threading.Lock): 线程锁，用于确保缓存存取操作的线程安全。
    """
    SUPPORTED_SOUND_FORMAT = ["flac", "m4a", "mp3", "wav"]
    CACHE_FILE = os.path.join(CACHE_PATH, "bk_asr", "asr_cache.json")
    _lock = threading.Lock()

    def __init__(self,
                 audio_path: Optional[Union[str, bytes]] = None,
                 use_cache: bool = False,
                 # need_word_time_stamp: bool = False,
                 log_to_ui_func=None):
        """初始化实例。

        Args:
            audio_path (Optional[Union[str, bytes]]): 音频文件路径或字节流。
            use_cache (bool): 是否使用缓存。
            # need_word_time_stamp (bool): 是否需要字级时间戳。
            log_to_ui_func (callable, optional): 用于记录日志到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)
        self.audio_path = audio_path
        self.file_binary = None

        self.crc32_hex = None
        self.use_cache = use_cache
        self._set_data()

        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        """加载缓存文件。

        Returns:
            dict: 缓存数据字典。
        """
        if not self.use_cache:
            return {}
        os.makedirs(os.path.dirname(self.CACHE_FILE), exist_ok=True)
        with self._lock:
            if os.path.exists(self.CACHE_FILE):
                try:
                    with open(self.CACHE_FILE, 'r', encoding='utf-8') as f:
                        cache = json.load(f)
                        if isinstance(cache, dict):
                            return cache
                except (json.JSONDecodeError, IOError):
                    return {}
            return {}

    def _save_cache(self) -> None:
        """保存缓存到文件。"""
        if not self.use_cache:
            return
        with self._lock:
            try:
                with open(self.CACHE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.cache, f, ensure_ascii=False, indent=2)
                # 如果缓存文件大于 20MB，删除缓存文件
                if os.path.exists(self.CACHE_FILE) and os.path.getsize(self.CACHE_FILE) > 20 * 1024 * 1024:
                    os.remove(self.CACHE_FILE)
            except IOError:
                pass

    def _set_data(self) -> None:
        """设置音频数据和 CRC32 校验码。"""
        if isinstance(self.audio_path, bytes):
            # 如果传入的是字节流
            self.file_binary = self.audio_path
        else:
            # 如果传入的是文件路径
            ext = self.audio_path.split(".")[-1].lower()
            assert ext in self.SUPPORTED_SOUND_FORMAT, f"不支持的音频格式: {ext}"
            assert os.path.exists(self.audio_path), f"文件未找到: {self.audio_path}"
            with open(self.audio_path, "rb") as f:
                self.file_binary = f.read()
        crc32_value = zlib.crc32(self.file_binary) & 0xFFFFFFFF
        self.crc32_hex = format(crc32_value, '08x')

    def _get_key(self) -> str:
        """获取缓存键值。

        Returns:
            str: 缓存键值。
        """
        return f"{self.__class__.__name__}-{self.crc32_hex}"

    def run(self, callback=None, **kwargs) -> ASRData:
        """运行 ASR 服务并返回结果。

        Args:
            callback (callable, optional): 回调函数。
            **kwargs: 其他参数。

        Returns:
            ASRData: ASR 结果数据。
        """
        key = self._get_key()
        if key in self.cache and self.use_cache:
            resp_data = self.cache[key]
        else:
            resp_data = self._run(callback, **kwargs)
            # 缓存结果
            self.cache[key] = resp_data
            self._save_cache()
        segments = self._make_segments(resp_data)
        return ASRData(segments)

    def _make_segments(self, resp_data: dict) -> list[ASRDataSeg]:
        """根据响应数据创建 ASRDataSeg 列表。

        Args:
            resp_data (dict): 响应数据。

        Returns:
            list[ASRDataSeg]: ASRDataSeg 列表。

        Raises:
            NotImplementedError: 必须在子类中实现此方法。
        """
        raise NotImplementedError("_make_segments 方法必须在子类中实现")

    def _run(self, callback=None, **kwargs):
        """运行 ASR 服务并返回响应数据。

        Args:
            callback (callable, optional): 回调函数。
            **kwargs: 其他参数。

        Raises:
            NotImplementedError: 必须在子类中实现此方法。
        """
        raise NotImplementedError("_run 方法必须在子类中实现")
