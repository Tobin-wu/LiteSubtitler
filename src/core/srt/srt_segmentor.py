# coding: utf8
import re
from typing import List, Optional

from core.asr.asr_data_seg import ASRDataSeg
from core.base_object import BaseObject
from utils.string_utils import StringUtils


class SubtitleProcessError(Exception):
    """字幕处理相关的异常"""
    pass


class SrtSegmentor(BaseObject):
    """
    字幕分段处理器，用于将 ASR 数据分段处理为更小的逻辑单元。

    主要功能：
        1. 预处理分段，移除无效内容。
        2. 根据时间间隔和常见连接词规则进行分段。
        3. 处理过长的分段，确保每段不超过最大词数限制。
    """

    # 常量定义
    SEGMENT_THRESHOLD = 500  # 每个分段的最大字数
    FIXED_NUM_THREADS = 1  # 固定的线程数量
    SPLIT_RANGE = 30  # 在分割点前后寻找最大时间间隔的范围
    MAX_GAP = 1500  # 允许每个词语之间的最大时间间隔（毫秒）
    USE_CACHE = True  # 是否使用缓存

    MAX_WORD_COUNT_ENGLISH = 10  # 英文最大单词数
    MAX_WORD_COUNT_CJK = 15  # 中日韩文字最大字数

    DEFAULT_WINDOW_SIZE = 5  # 检查最近5个间隔

    # 常见连接词集合
    PREFIX_SPLIT_WORDS = {
        # 英文冠词
        "a", "an", "the",
        # 英文连接词和介词
        "and", "or", "but", "if", "then", "because", "as", "until", "while",
        "when", "where", "nor", "yet", "so", "for", "however", "moreover",
        "furthermore", "therefore", "thus", "although", "though", "nevertheless",
        "meanwhile", "consequently", "additionally", "besides", "instead", "unless",
        "since", "before", "after", "during", "within", "without", "up", "down",
        "out", "off", "into", "onto", "upon", "toward", "against", "near",
        "inside", "outside", "across", "around", "behind", "beyond", "beside",
        "beneath", "except",
        # 英文代词（主格和宾格）
        "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them",
        # 英文物主代词和指示代词
        "my", "your", "his", "her", "its", "our", "their",
        "that", "this", "these", "those",
        "what", "who", "whom", "whose", "which", "why", "how",
        # 英文介词
        "in", "on", "at", "to", "for", "with", "by", "from",
        "about", "above", "below", "under", "over",
        "through", "between", "among",
        # 中文并列连词
        "和", "及", "与", "但", "而", "或", "因",
        # 中文人称代词
        "我", "你", "他", "她", "它", "咱", "您", "这", "那", "哪"
    }

    SUFFIX_SPLIT_WORDS = {
        # 标点符号
        ".", ",", "!", "?", "。", "，", "！", "？",
        # 英文所有格代词
        "mine", "yours", "his", "hers", "its", "ours", "theirs",
        # 英文副词
        "too", "either", "neither",
        # 中文语气词和助词
        "的", "了", "着", "过", "吗", "呢", "吧", "啊", "呀", "哦", "哈", "嘛", "啦"
    }

    def __init__(self, log_to_ui_func: Optional[callable] = None):
        """
        初始化字幕分段处理器。

        Args:
            log_to_ui_func: 日志输出函数，用于将日志信息输出到 UI。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)

    def preprocess_segments(self, segments: List[ASRDataSeg], need_lower: bool = True) -> List[ASRDataSeg]:
        """
        预处理 ASR 数据分段：
            1. 移除纯标点符号的分段。
            2. 对仅包含字母、数字和撇号的文本进行小写处理并添加空格。

        Args:
            segments: ASR 数据分段列表。
            need_lower: 是否需要对文本进行小写处理。

        Returns:
            处理后的分段列表。
        """
        self.log_info(f"预处理 ASR 数据分段: {len(segments)}")
        new_segments = []
        for seg in segments:
            if not StringUtils.is_pure_punctuation(seg.text):
                # 如果文本只包含字母、数字和撇号，则将其转换为小写并添加一个空格
                if re.match(r'^[a-zA-Z0-9\']+$', seg.text.strip()):
                    seg.text = seg.text.lower() + " " if need_lower else seg.text + " "
                new_segments.append(seg)
        return new_segments

    def process_by_rules(self, segments: List[ASRDataSeg]) -> List[ASRDataSeg]:
        """
        使用规则进行基础的句子分割。

        规则包括：
            1. 考虑时间间隔，超过阈值的进行分割。
            2. 在常见连接词前后进行分割（保证分割后两个分段都大于 5 个单词）。
            3. 分割大于 MAX_WORD_COUNT 个单词的分段。

        Args:
            segments: ASR 数据分段列表。

        Returns:
            处理后的分段列表。
        """
        self.log_info(f"分段: {len(segments)}")
        # 1. 先按时间间隔分组
        segment_groups = self._merge_by_time_gaps(segments, max_gap=500, check_large_gaps=True)
        self.log_info(f"按时间间隔分组: {len(segment_groups)}")

        # 2. 按常用词分割，只处理长句
        common_result_groups = []
        for group in segment_groups:
            max_word_count = self._get_max_word_count(group)
            if StringUtils.count_words("".join(seg.text for seg in group)) > max_word_count:
                segments = self._merge_common_words(group)
                common_result_groups.extend(segments)
            else:
                common_result_groups.append(group)

        # 3. 处理过长的分段
        result_segments = []
        for group in common_result_groups:
            result_segments.extend(self._split_long_segment(group))

        return result_segments

    def _get_max_word_count(self, segments: List[ASRDataSeg]) -> int:
        """
        根据文本类型获取最大词数限制。

        Args:
            segments: ASR 数据分段列表。

        Returns:
            最大词数限制。
        """
        merged_text = "".join(seg.text for seg in segments)
        return self.MAX_WORD_COUNT_CJK if StringUtils.is_mainly_cjk(merged_text) else self.MAX_WORD_COUNT_ENGLISH

    def _split_long_segment(self, segs_to_merge: List[ASRDataSeg]) -> List[ASRDataSeg]:
        """
        基于最大时间间隔拆分长分段，根据文本类型使用不同的最大词数限制。

        Args:
            segs_to_merge: 待合并的分段列表。

        Returns:
            拆分后的分段列表。
        """
        if not segs_to_merge:
            return []

        merged_text = "".join(seg.text for seg in segs_to_merge)
        max_word_count = self._get_max_word_count(segs_to_merge)

        # 如果分段足够短或无法进一步拆分
        if StringUtils.count_words(merged_text) <= max_word_count or len(segs_to_merge) == 1:
            merged_seg = ASRDataSeg(
                merged_text.strip(),
                segs_to_merge[0].start_time,
                segs_to_merge[-1].end_time
            )
            return [merged_seg]

        # 检查时间间隔是否都相等
        n = len(segs_to_merge)
        gaps = [segs_to_merge[i + 1].start_time - segs_to_merge[i].end_time for i in range(n - 1)]
        all_equal = all(abs(gap - gaps[0]) < 1e-6 for gap in gaps)

        # 确定分割点
        split_index = n // 2 if all_equal else self._find_split_index(segs_to_merge, n)

        # 递归拆分
        first_segs = segs_to_merge[:split_index]
        second_segs = segs_to_merge[split_index:]
        return self._split_long_segment(first_segs) + self._split_long_segment(second_segs)

    @staticmethod
    def _find_split_index(segments: List[ASRDataSeg], total_segments: int) -> int:
        """
        在分段中间 2/3 部分寻找最大时间间隔点。

        Args:
            segments: 分段列表。
            total_segments: 分段总数。

        Returns:
            分割点的索引。
        """
        start_idx = total_segments // 6
        end_idx = (5 * total_segments) // 6
        return max(
            range(start_idx, end_idx),
            key=lambda i: segments[i + 1].start_time - segments[i].end_time,
            default=total_segments // 2
        )

    def _merge_by_time_gaps(self,
                            segments: List[ASRDataSeg],
                            max_gap: int = MAX_GAP,
                            check_large_gaps: bool = False) -> List[List[ASRDataSeg]]:
        """
        检查字幕分段之间的时间间隔，如果超过阈值则分段。

        Args:
            segments: 待检查的分段列表。
            max_gap: 最大允许的时间间隔（毫秒）。
            check_large_gaps: 是否检查连续的大时间间隔。

        Returns:
            分段后的列表的列表。
        """
        if not segments:
            return []

        result = []
        current_group = [segments[0]]
        recent_gaps = []  # 存储最近的时间间隔

        for i in range(1, len(segments)):
            time_gap = segments[i].start_time - segments[i - 1].end_time

            if check_large_gaps:
                recent_gaps.append(time_gap)
                if len(recent_gaps) > self.DEFAULT_WINDOW_SIZE:
                    recent_gaps.pop(0)
                if len(recent_gaps) == self.DEFAULT_WINDOW_SIZE:
                    avg_gap = sum(recent_gaps) / len(recent_gaps)
                    # 如果当前间隔大于平均值的 3 倍
                    if time_gap > avg_gap * 3 and len(current_group) > 5:
                        self.log_debug(f"检测到大间隔: {time_gap}ms, 平均间隔: {avg_gap}ms")
                        result.append(current_group)
                        current_group = []
                        recent_gaps = []  # 重置间隔记录

            if time_gap > max_gap:
                self.log_debug(f"超过阈值，分组: {''.join(seg.text for seg in current_group)}")
                result.append(current_group)
                current_group = []
                recent_gaps = []  # 重置间隔记录

            current_group.append(segments[i])

        if current_group:
            result.append(current_group)

        return result

    def _merge_common_words(self, segments: List[ASRDataSeg]) -> List[List[ASRDataSeg]]:
        """
        在常见连接词前后进行分割，确保分割后的每个分段都至少有 5 个单词。

        Args:
            segments: ASR 数据分段列表，每个 segment 包含一个词。

        Returns:
            分组后的分段列表的列表。
        """
        result = []
        current_group = []

        for i, seg in enumerate(segments):
            max_word_count = self._get_max_word_count([seg])
            if self._should_split_at_prefix(seg.text, current_group, max_word_count):
                result.append(current_group)
                self.log_debug(f"在前缀词 {seg.text} 前分割 - {''.join(seg.text for seg in current_group)}")
                current_group = []

            if self._should_split_at_suffix(segments, i, current_group, max_word_count):
                result.append(current_group)
                self.log_debug(f"在后缀词 {segments[i - 1].text} 后分割 - {''.join(seg.text for seg in current_group)}")
                current_group = []

            current_group.append(seg)

        if current_group:
            result.append(current_group)

        return result

    def _should_split_at_prefix(self, text: str, current_group: List[ASRDataSeg], max_word_count: int) -> bool:
        """
        判断是否需要在当前词前分割。

        Args:
            text: 当前词的文本。
            current_group: 当前分组。
            max_word_count: 最大词数限制。

        Returns:
            是否需要在当前词前分割。
        """
        return (any(text.lower().startswith(word) for word in self.PREFIX_SPLIT_WORDS)
                and len(current_group) >= int(max_word_count * 0.6))

    def _should_split_at_suffix(self,
                                segments: List[ASRDataSeg],
                                index: int,
                                current_group: List[ASRDataSeg],
                                max_word_count: int) -> bool:
        """
        判断是否需要在当前词后分割。

        Args:
            segments: 分段列表。
            index: 当前词的索引。
            current_group: 当前分组。
            max_word_count: 最大词数限制。

        Returns:
            是否需要在当前词后分割。
        """
        return (index > 0
                and any(segments[index - 1].text.lower().endswith(word) for word in self.SUFFIX_SPLIT_WORDS)
                and len(current_group) >= int(max_word_count * 0.4))
