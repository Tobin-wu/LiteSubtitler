# coding: utf8
import re
from PyQt6.QtGui import QColor


class StyleUtils:
    """样式工具类，提供样式字符串处理功能。"""

    @staticmethod
    def background_color_in_stylesheet(style_str: str) -> QColor | None:
        """从样式字符串中提取背景颜色值。

        支持以下颜色格式：
        - 十六进制颜色（如 `#RRGGBB`）
        - RGB 颜色（如 `rgb(R, G, B)`）
        - RGBA 颜色（如 `rgb(R, G, B / A)`）

        Args:
            style_str (str): 样式字符串。

        Returns:
            QColor: 提取的背景颜色值。如果未找到或无效，则返回 `None`。
        """
        # 正则表达式匹配背景颜色值，支持十六进制和 RGB/RGBA 格式
        match = re.search(
            r'background-color:\s*'
            r'(#[\da-fA-F]{6}|'  # 十六进制颜色
            r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'  # RGB 颜色
            r'(?:\s*/\s*(\d+\.?\d*)\s*)?'  # 可选的 Alpha 通道
            r');',  # 结束分号
            style_str
        )

        if not match:
            return None

        # 处理十六进制颜色
        if match.group(1) and match.group(1).startswith('#'):
            color_value = match.group(1)
            color = QColor(color_value)
        # 处理 RGB/RGBA 颜色
        elif match.group(2) and match.group(3) and match.group(4):
            r = int(match.group(2))
            g = int(match.group(3))
            b = int(match.group(4))
            color = QColor(r, g, b)
        else:
            return None

        # 返回有效的颜色对象
        return color if color.isValid() else None
