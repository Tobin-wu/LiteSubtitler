# coding: utf8
import uuid


class UuidUtils:
    """UUID 工具类，提供 UUID 生成和格式化功能。"""

    @staticmethod
    def generate_guid() -> str:
        """生成一个不带连字符的 UUID 版本 4 字符串。

        UUID 版本 4 是基于随机数的 UUID，具有极高的唯一性。
        生成的 UUID 字符串会去除连字符（`-`），适合需要紧凑格式的场景。

        Returns:
            str: 不带连字符的 UUID 字符串。
        """
        # 生成 UUID 版本 4
        unique_id = uuid.uuid4()

        # 将 UUID 对象转换为字符串并移除连字符
        unique_id_str = unique_id.hex

        return unique_id_str
