# coding: utf8
import os
import sys
import logging
import json
from typing import Dict, Any, List, Optional

VERSION = "v1.0.0"
APP_NAME = "LiteSubtitler"
AUTHOR = "Tobin.wu"

HELP_URL = "https://github.com/Tobin-wu/LiteSubtitler"
GITHUB_REPO_URL = "https://github.com/Tobin-wu/LiteSubtitler"
RELEASE_URL = "https://github.com/Tobin-wu/LiteSubtitler/releases/latest"
FEEDBACK_URL = "https://github.com/Tobin-wu/LiteSubtitler/issues"

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 确保当前工作目录为 exe 文件所在目录
if getattr(sys, 'frozen', False):
    # 如果是打包后的可执行文件
    ROOT_PATH = os.path.dirname(sys.executable)

RESOURCE_PATH = os.path.join(ROOT_PATH, "resources")
APPDATA_PATH = os.path.join(ROOT_PATH, "AppData")

CACHE_PATH = os.path.join(APPDATA_PATH, "cache")
TEMP_PATH = os.path.join(APPDATA_PATH, "temp")

SETTING_PATH = os.path.join(ROOT_PATH, "setting.json")
PROMPT_PATH = os.path.join(RESOURCE_PATH, "prompts")

ICON_REC = {
    "add": os.path.join(RESOURCE_PATH, "images", "icons", "plus.png"),
    "run": os.path.join(RESOURCE_PATH, "images", "icons", "启动.png"),
    "stop": os.path.join(RESOURCE_PATH, "images", "icons", "暂停.png"),
    "clear": os.path.join(RESOURCE_PATH, "images", "icons", "清空.png"),
    "download": os.path.join(RESOURCE_PATH, "images", "icons", "下载.png"),
    "download-model": os.path.join(RESOURCE_PATH, "images", "icons", "下载模型.png"),
    "register-llm": os.path.join(RESOURCE_PATH, "images", "icons", "注册.png"),
    "file": os.path.join(RESOURCE_PATH, "images", "icons", "可执行文件.png"),
    "dir": os.path.join(RESOURCE_PATH, "images", "icons", "文件夹.png"),
    "link": os.path.join(RESOURCE_PATH, "images", "icons", "link.png"),
    "save-setting": os.path.join(RESOURCE_PATH, "images", "icons", "设置.png"),
    "color": os.path.join(RESOURCE_PATH, "images", "icons", "color.png"),
    "setting-show": os.path.join(RESOURCE_PATH, "images", "icons", "显示.png"),
    "setting-hide": os.path.join(RESOURCE_PATH, "images", "icons", "隐藏.png"),
    "refresh": os.path.join(RESOURCE_PATH, "images", "icons", "更新.png"),
}

DEFAULT_ARGS = {
    "LOG_SETTING": {
        'path': os.path.join(APPDATA_PATH, "logs"),
        'level': logging.INFO,
        'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "asr_args": {
        "use_cache": False,
        "faster_whisper_path": os.path.join(ROOT_PATH, "Faster-Whisper-XXL", "faster-whisper-xxl.exe"),
        "whisper_model": "small",  # "large-v2",
        "model_dir": os.path.join(ROOT_PATH, "models"),
        "device": "cpu",  # cuda or cpu
        "vad_filter": False,
        "vad_threshold": 0.2,
        "vad_method": "silero_v3",
        "ff_mdx_kim2": True,  # 分离出人声
        "language": "auto"  # 源语言
    },
    "translate_args": {
        "need_translate": True,  # 是否翻译
        "translate_mode": "精细翻译",
        "source_language": "",  # 源语言
        "target_language": "简体中文",  # 目标语言
        # "llm_api_url": "http://127.0.0.1:11434/v1",
        # "llm_api_key": "api.key",
        # "llm_model": "gemma2:latest",  # 模型
        "llm_api_url": "https://api.siliconflow.cn/v1",
        "llm_api_key": "sk-wlyrgyaimjzndvavtogmqssbjdajdvdkzpqbeiyrqaoeivno",
        "llm_model": "THUDM/glm-4-9b-chat",  # "gemma2:latest",  # 模型
        "need_remove_punctuation": True,  # 是否删除句子中的符号
    },
    "subtitle_args": {
        "subtitle_layout": "译文在上",  # 字幕排布，哪个是主字幕，哪个是副字幕，在上面的是主字幕
        "subtitle_margin_v": 20,  # 垂直间距，字幕和视频底部之间的距离
        "is_embed_subtitle": True,  # 是否合成到视频
        "is_soft_subtitle": False,  # 是否软字幕
        "need_remove_temp_file": True,  # 需要删除中间临时文件
        "default_style": {  # 主字幕样式
            "Name": "Default",  # Secondary
            "Fontname": "微软雅黑",  # 字体
            "Fontsize": 50,  # 字号
            "PrimaryColour": "#5aff65",  # 字幕主颜色
            "SecondaryColour": "#0000FF",  #
            "OutlineColour": "#000000",  # 字幕边框颜色
            "BackColour": "#000000",  # 字幕背景颜色
            "Bold": -1,  # 加粗, -1 无效，0 不加，1 加粗
            "Italic": 0,  # 斜体, 0 不斜体，1 斜体
            "Underline": 0,  # 下划线
            "StrikeOut": 0,  # 删除线
            "ScaleX": 100,  # X轴缩放比例
            "ScaleY": 100,  # Y轴缩放比例
            "Spacing": 2.0,  # 间距, 字与字之间的间距
            "Angle": 0,  # 角度
            "BorderStyle": 1,  # 边框样式
            "Outline": 2.0,  # 轮廓尺寸，每个字的轮廓尺寸
            "Shadow": 0,  # 阴影
            "Alignment": 2,  # 对齐方式
            "MarginL": 10,  # 左边距
            "MarginR": 10,  # 右边距
            "MarginV": 20,  # 垂直边距, 就是 subtitle_margin_v
            "Encoding": 1  # 编码
        },
        "secondary_style": {  # 副字幕样式
            "Name": "Secondary",
            "Fontname": "微软雅黑",  # 字体
            "Fontsize": 36,  # 字号
            "PrimaryColour": "#38c3ff",  # 字幕主颜色
            "SecondaryColour": "#0000FF",  #
            "OutlineColour": "#000000",  # 字幕边框颜色
            "BackColour": "#000000",  # 字幕背景颜色
            "Bold": -1,  # 加粗, -1 无效，0 不加，1 加粗
            "Italic": 0,  # 斜体, 0 不斜体，1 斜体
            "Underline": 0,  # 下划线
            "StrikeOut": 0,  # 删除线
            "ScaleX": 100,  # X轴缩放比例
            "ScaleY": 100,  # Y轴缩放比例
            "Spacing": 2.0,  # 间距, 字与字之间的间距
            "Angle": 0,  # 角度
            "BorderStyle": 1,  # 边框样式
            "Outline": 2.0,  # 轮廓尺寸，每个字的轮廓尺寸
            "Shadow": 0,  # 阴影
            "Alignment": 2,  # 对齐方式
            "MarginL": 10,  # 左边距
            "MarginR": 10,  # 右边距
            "MarginV": 20,  # 垂直边距, 就是 subtitle_margin_v
            "Encoding": 1  # 编码
        },
    }
}


class ConfigTool:
    """配置工具类，用于读取、保存和操作配置文件。"""

    @staticmethod
    def read_config_setting() -> Dict[str, Any]:
        """读取配置文件内容。

        如果配置文件存在，则读取并返回其内容；如果不存在，则返回默认配置。

        Returns:
            Dict[str, Any]: 配置文件的字典形式内容或默认配置。
        """
        if os.path.exists(SETTING_PATH):
            with open(SETTING_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        return DEFAULT_ARGS.copy()

    @staticmethod
    def save_config_setting(config_args: Dict[str, Any]) -> None:
        """保存配置到文件。

        Args:
            config_args (Dict[str, Any]): 需要保存的配置字典。
        """
        with open(SETTING_PATH, 'w', encoding='utf-8') as file:
            json.dump(config_args, file, ensure_ascii=False, indent=4)

    @staticmethod
    def reset_config_attr(config_dict: Dict[str, Any], key_path: List[str], the_value: Any) -> None:
        """重置配置字典中的某个属性值。

        Args:
            config_dict (Dict[str, Any]): 配置字典。
            key_path (List[str]): 属性路径，例如 ['section', 'key']。
            the_value (Any): 需要设置的值。
        """
        current_dict = config_dict
        for i, key in enumerate(key_path):
            if i == len(key_path) - 1:
                current_dict[key] = the_value
            else:
                current_dict = current_dict.setdefault(key, {})

    @staticmethod
    def read_config_attr(config_dict: Dict[str, Any], key_path: List[str]) -> Optional[Any]:
        """读取配置字典中的某个属性值。

        Args:
            config_dict (Dict[str, Any]): 配置字典。
            key_path (List[str]): 属性路径，例如 ['section', 'key']。

        Returns:
            Optional[Any]: 属性值，如果路径不存在则返回 '0'。
        """
        current_dict = config_dict
        for i, key in enumerate(key_path):
            if i == len(key_path) - 1:
                return current_dict.get(key, '0')
            current_dict = current_dict.setdefault(key, {})
        return None
