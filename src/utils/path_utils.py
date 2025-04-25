# coding: utf8
import os
import re


class PathUtils:
    """路径工具类，提供与系统路径相关的常用方法。"""

    @staticmethod
    def have_space(file_path: str) -> bool:
        return re.search(r"\s", file_path)

    @staticmethod
    def append_to_env_path(target_path: str) -> None:
        """将目标路径添加到系统的环境变量 PATH 中（如果尚未存在）。

        Args:
            target_path (str): 需要添加到 PATH 的路径。
        """
        if not PathUtils.is_path_in_env_path(target_path):
            os.environ["PATH"] = target_path + os.pathsep + os.environ["PATH"]

    @staticmethod
    def is_path_in_env_path(target_path: str) -> bool:
        """检查目标路径是否已经存在于系统的环境变量 PATH 中。

        Args:
            target_path (str): 需要检查的路径。

        Returns:
            bool: 如果目标路径存在于 PATH 中，返回 True；否则返回 False。
        """
        # 获取当前的环境变量 PATH，默认为空字符串
        env_path = os.environ.get("PATH", "")

        # 将 PATH 按路径分隔符分割成列表
        paths = env_path.split(os.pathsep)

        # 检查目标路径是否在列表中
        return target_path in paths
