# coding: utf8
from typing import Dict, Any


class DictUtils:
    """字典工具类，提供字典相关的常用方法。"""

    @staticmethod
    def update_by_key(org_dict: Dict[Any, Any], upt_dict: Dict[Any, Any]) -> None:
        """用 `upt_dict` 更新 `org_dict`，仅更新 `org_dict` 中已存在的键。

        该方法会遍历 `upt_dict`，如果某个键在 `org_dict` 中存在，则更新其值。

        Args:
            org_dict (Dict[Any, Any]): 原始字典，将被更新。
            upt_dict (Dict[Any, Any]): 更新字典，提供新的键值对。
        """
        # 仅更新 org_dict 中已存在的键
        for key, value in upt_dict.items():
            if key in org_dict:
                org_dict[key] = value


if __name__ == "__main__":
    # 示例用法
    org = {
        "use_cache": False,
        "need_word_time_stamp": True,
        "faster_whisper_path": "D:/tools/ai/Faster-Whisper-XXL/faster-whisper-xxl.exe",
        "whisper_model": "large-v2",
        "model_dir": "D:/tools/ai/models",
        "device": "cuda",  # cuda or cpu
        "vad_filter": False,
        "vad_threshold": 0.2,
        "vad_method": "silero_v3",
        "ff_mdx_kim2": True,  # 分离出人声
        "one_word": True,
        "sentence": False,
        "language": "en",
        "prompt": ""
    }

    # 更新字典
    DictUtils.update_by_key(org, {"language": "zh", "one_word": False, "prompt": "hello"})
    print(org)
