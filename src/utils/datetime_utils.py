# coding: utf8
from datetime import datetime


class DatetimeUtils:
    """日期时间工具类，提供日期时间相关的常用方法。"""

    @staticmethod
    def now_datetime() -> str:
        """获取当前日期和时间，格式化为精确到毫秒的字符串。

        Returns:
            str: 当前日期时间的字符串，格式为 'YYYY-MM-DD HH:MM:SS.sss'。
        """
        now = datetime.now()
        # 格式化为精确到毫秒的字符串，并截取前3位毫秒
        return now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    @staticmethod
    def str_to_datetime(date_str: str) -> datetime:
        """将字符串转换为 datetime 对象。

        Args:
            date_str (str): 日期时间字符串，格式为 'YYYY-MM-DD HH:MM:SS.sss'。

        Returns:
            datetime: 转换后的 datetime 对象。
        """
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
