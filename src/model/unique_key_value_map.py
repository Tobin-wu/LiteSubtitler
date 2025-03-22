# coding: utf8
from typing import Any, Optional, Dict, Union, List


class UniqueKeyValueMap:
    """
    双向映射类，用于维护键和值之间的唯一映射关系。

    主要功能：
        1. 支持添加键值对，确保键和值的唯一性。
        2. 支持通过键获取值，或通过值获取键。
        3. 支持删除键值对。
    """

    def __init__(self):
        """
        初始化双向映射类。
        """
        self.key_to_value: Dict[Any, Any] = {}  # 键到值的映射
        self.value_to_key: Dict[Any, Any] = {}  # 值到键的映射

    def add(self, key: Any, value: Any) -> None:
        """
        添加键值对，确保键和值的唯一性。

        Args:
            key: 键。
            value: 值。

        Raises:
            KeyError: 如果键已存在。
            ValueError: 如果值已存在。
        """
        if key in self.key_to_value:
            raise KeyError(f"键 '{key}' 已存在。")
        if value in self.value_to_key:
            raise ValueError(f"值 '{value}' 已与其他键关联。")
        self.key_to_value[key] = value
        self.value_to_key[value] = key

    def get_value_from_key(self, key: Any) -> Optional[Any]:
        """
        通过键获取值。

        Args:
            key: 键。

        Returns:
            对应的值，如果键不存在则返回 None。
        """
        return self.key_to_value.get(key, None)

    def get_key_from_value(self, value: Any) -> Union[Optional[Any], List[Any]]:
        """
        通过值获取键。

        Args:
            value: 值。

        Returns:
            对应的键，如果值不存在则返回 None。
            如果键是元组类型，则返回列表形式。
        """
        key = self.value_to_key.get(value, None)
        if key and isinstance(key, tuple):
            return list(key)
        return key

    def remove(self, key: Any) -> None:
        """
        删除键值对。

        Args:
            key: 要删除的键。
        """
        value = self.key_to_value.pop(key, None)
        if value is not None:
            self.value_to_key.pop(value, None)