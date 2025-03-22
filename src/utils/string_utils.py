# coding: utf8
import re


class StringUtils:
    """字符串处理工具类，提供多种字符串处理功能。"""

    @staticmethod
    def is_pure_punctuation(text: str) -> bool:
        """检查字符串是否仅由标点符号组成。

        Args:
            text (str): 输入的字符串。

        Returns:
            bool: 如果字符串仅由标点符号组成，则返回True，否则返回False。
        """
        return not re.search(r'\w', text, flags=re.UNICODE)

    @staticmethod
    def is_mainly_cjk(text: str) -> bool:
        """判断文本是否主要由中日韩文字组成。

        Args:
            text (str): 输入的文本。

        Returns:
            bool: 如果CJK字符占比超过50%，则返回True，否则返回False。
        """
        # 定义CJK字符的Unicode范围
        cjk_patterns = [
            r'[\u4e00-\u9fff]',  # 中日韩统一表意文字
            r'[\u3040-\u309f]',  # 平假名
            r'[\u30a0-\u30ff]',  # 片假名
            r'[\uac00-\ud7af]',  # 韩文音节
        ]

        # 计算CJK字符数
        cjk_count = sum(len(re.findall(pattern, text)) for pattern in cjk_patterns)

        # 计算总字符数（不包括空白字符）
        total_chars = len(''.join(text.split()))

        # 如果CJK字符占比超过50%，则认为主要是CJK文本
        return cjk_count / total_chars > 0.5 if total_chars > 0 else False

    @staticmethod
    def count_words(text: str) -> int:
        """统计多语言文本中的字符/单词数。

        支持:
        - 英文（按空格分词）
        - CJK文字（中日韩统一表意文字）
        - 韩文/谚文
        - 泰文
        - 阿拉伯文
        - 俄文西里尔字母
        - 希伯来文
        - 越南文
        每个字符都计为1个单位，英文按照空格分词计数。

        Args:
            text (str): 输入的文本。

        Returns:
            int: 文本中的字符/单词总数。
        """
        # 定义各种语言的Unicode范围
        patterns = [
            r'[\u4e00-\u9fff]',  # 中日韩统一表意文字
            r'[\u3040-\u309f]',  # 平假名
            r'[\u30a0-\u30ff]',  # 片假名
            r'[\uac00-\ud7af]',  # 韩文音节
            r'[\u0e00-\u0e7f]',  # 泰文
            r'[\u0600-\u06ff]',  # 阿拉伯文
            r'[\u0590-\u05ff]',  # 希伯来文
            r'[\u1e00-\u1eff]',  # 越南文
            r'[\u3130-\u318f]',  # 韩文兼容字母
        ]

        # 统计所有非英文字符
        non_english_chars = 0
        remaining_text = text

        for pattern in patterns:
            # 计算当前语言的字符数
            chars = len(re.findall(pattern, remaining_text))
            non_english_chars += chars
            # 从文本中移除已计数的字符
            remaining_text = re.sub(pattern, ' ', remaining_text)

        # 计算英文单词数（处理剩余的文本）
        english_words = len(remaining_text.strip().split())

        return non_english_chars + english_words
