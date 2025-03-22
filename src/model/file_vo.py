# coding: utf8
import os


class FileVO:
    """
    文件值对象类，用于封装文件路径及其相关属性。

    主要功能：
        1. 解析文件路径，提取文件名、扩展名、目录等信息。
        2. 提供文件属性的只读访问。
    """

    def __init__(self, file_path: str):
        """
        初始化文件值对象。

        Args:
            file_path: 文件路径。
        """
        # 初始化所有实例属性
        self._file_path = file_path
        self._is_file = False
        self._file_dir = ""
        self._file_name = ""
        self._file_only_name = ""
        self._file_extension = ""

        # 解析文件路径
        self._parse_file_path()

    def _parse_file_path(self) -> None:
        """
        解析文件路径，提取文件名、扩展名、目录等信息。

        解析结果会存储在实例属性中：
            - is_file: 是否为文件。
            - file_dir: 文件所在目录。
            - file_name: 文件名（包含扩展名）。
            - file_only_name: 文件名（不包含扩展名）。
            - file_extension: 文件扩展名（不包含点，转换为小写）。
        """
        self._is_file = os.path.isfile(self._file_path)
        self._file_dir = os.path.dirname(self._file_path)
        self._file_name = os.path.basename(self._file_path)
        self._file_only_name, self._file_extension = self._split_file_name(self._file_name)

    @staticmethod
    def _split_file_name(file_name: str) -> tuple[str, str]:
        """
        拆分文件名，返回文件名和扩展名。

        Args:
            file_name: 文件名（包含扩展名）。

        Returns:
            元组，包含文件名（不包含扩展名）和扩展名（不包含点，转换为小写）。
        """
        name, extension = os.path.splitext(file_name)
        return name, extension[1:].strip().lower()

    @property
    def file_path(self) -> str:
        """
        获取文件路径。

        Returns:
            文件路径。
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value: str) -> None:
        """
        设置文件路径，并重新解析文件属性。

        Args:
            value: 文件路径。
        """
        self._file_path = value
        self._parse_file_path()

    @property
    def is_file(self) -> bool:
        """
        判断是否为文件。

        Returns:
            是否为文件。
        """
        return self._is_file

    @is_file.setter
    def is_file(self, value: bool) -> None:
        """
        设置是否为文件。

        Args:
            value: 是否为文件。
        """
        self._is_file = value

    @property
    def file_dir(self) -> str:
        """
        获取文件所在目录。

        Returns:
            文件所在目录。
        """
        return self._file_dir

    @file_dir.setter
    def file_dir(self, value: str) -> None:
        """
        设置文件所在目录。

        Args:
            value: 文件所在目录。
        """
        self._file_dir = value

    @property
    def file_name(self) -> str:
        """
        获取文件名（包含扩展名）。

        Returns:
            文件名（包含扩展名）。
        """
        return self._file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        """
        设置文件名（包含扩展名）。

        Args:
            value: 文件名（包含扩展名）。
        """
        self._file_name = value

    @property
    def file_only_name(self) -> str:
        """
        获取文件名（不包含扩展名）。

        Returns:
            文件名（不包含扩展名）。
        """
        return self._file_only_name

    @file_only_name.setter
    def file_only_name(self, value: str) -> None:
        """
        设置文件名（不包含扩展名）。

        Args:
            value: 文件名（不包含扩展名）。
        """
        self._file_only_name = value

    @property
    def file_extension(self) -> str:
        """
        获取文件扩展名（不包含点，转换为小写）。

        Returns:
            文件扩展名（不包含点，转换为小写）。
        """
        return self._file_extension

    @file_extension.setter
    def file_extension(self, value: str) -> None:
        """
        设置文件扩展名（不包含点，转换为小写）。

        Args:
            value: 文件扩展名（不包含点，转换为小写）。
        """
        self._file_extension = value
