# coding: utf8
import re
from typing import Dict, List


class SrtTool:
    """SRT 工具类，用于解析对话记录和分组字幕。

    该类提供了两个静态方法：
    1. `parse_chat_records`: 解析对话记录并提取时间、说话者和文本。
    2. `group_subtitles`: 对字幕字典进行分组，支持重叠分组。
    """

    @staticmethod
    def parse_chat_records(chat_record: str) -> List[Dict]:
        """解析对话记录并提取时间、说话者和文本。

        Args:
            chat_record (str): 对话记录字符串，包含多行对话。

        Returns:
            List[Dict]: 解析后的对话记录列表，每个元素是一个字典，包含以下键：
                - seqNo: 序列号。
                - start: 对话开始时间。
                - end: 对话结束时间。
                - text: 对话文本。
                - speaker: 说话者。
        """
        # 定义正则表达式匹配对话记录中的每一行
        dialog_line_regex = re.compile(
            r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}) ([^:]+): (.+)'
        )

        items = []  # 存储解析后的对话记录
        seq_no = 1  # 序列号计数器

        for line in chat_record.splitlines():
            match = dialog_line_regex.match(line)
            if match:
                start_time, end_time, speaker, text = match.groups()
                item = {
                    'seqNo': seq_no,
                    'start': start_time.replace(',', '.'),  # 将逗号替换为点以符合时间格式
                    'end': end_time.replace(',', '.'),  # 将逗号替换为点以符合时间格式
                    'text': text.strip(),  # 去除文本两侧的空白字符
                    'speaker': speaker
                }
                items.append(item)
                seq_no += 1

        return items

    @staticmethod
    def group_subtitles(org_dict: Dict[int, str], step: int, prev: int) -> List[Dict[int, str]]:
        """对字幕字典进行分组，支持重叠分组。

        Args:
            org_dict (Dict[int, str]): 原始字幕字典，键为序号，值为字幕文本。
            step (int): 每组字幕的基本大小。
            prev (int): 每组与前一组重叠的字幕数量。

        Returns:
            List[Dict[int, str]]: 分组后的字幕字典列表。
        """
        sorted_keys = sorted(org_dict.keys())  # 对字典的键进行排序
        initial_chunks = [
            sorted_keys[i:i + step] for i in range(0, len(sorted_keys), step)
        ]  # 按 step 大小分块

        org_chunks = []  # 存储最终的分组结果
        prev_end = []  # 保存前一组的最后 prev 个键

        for idx, chunk_obj in enumerate(initial_chunks):
            if idx > 0:
                # 当前组前追加前一组的最后 prev 个键
                current_chunk = prev_end + chunk_obj
            else:
                current_chunk = chunk_obj

            # 构建当前组的字典
            chunk_dict = {k: org_dict[k] for k in current_chunk}
            org_chunks.append(chunk_dict)

            # 更新 prev_end 为当前组的最后 prev 个键
            prev_end = current_chunk[-prev:] if len(current_chunk) >= prev else []

        return org_chunks
