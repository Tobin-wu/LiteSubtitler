# coding: utf8
from enum import Enum
from typing import Type, Any, List, Optional, Callable

from PyQt6.QtWidgets import QComboBox

from config import ConfigTool
from core.base_object import BaseObject


class BaseConfigFacade(BaseObject):
    """配置有关的外观类。"""

    def __init__(self, log_to_ui_func, config: dict):
        """初始化应用程序实例。"""
        super().__init__(log_to_ui_func=log_to_ui_func)
        # 系统配置信息
        self.config_args = config

    def _init_combobox_(self,
                        combobox: QComboBox,
                        the_enum: Type[Enum],
                        key_path: Optional[List[str]] = None,
                        default_value: Any = None,
                        func_set_config: Optional[Callable] = None,
                        filter_for_items: Optional[Callable] = None) -> None:
        """
        初始化QComboBox，填充枚举值并连接信号槽。

        Args:
            combobox (QComboBox): 要初始化的QComboBox实例。
            the_enum (Type[Enum]): 枚举类，用于填充QComboBox的选项。
            key_path (Optional[List[str]]): 配置字典中的键路径，用于更新配置。
            default_value (Any): 默认值，当键路径不存在时使用。
            func_set_config (Optional[Callable]): 设置配置的函数。
            filter_for_items (Optional[Callable]): 下拉列表项目的过滤器。
        """
        # 设置QComboBox的下拉列表项之间的间隔
        combobox.view().setSpacing(2)

        # 填充QComboBox
        if filter_for_items:
            for member in the_enum:
                if filter_for_items(member.value):
                    combobox.addItem(member.value, member)
        else:
            for member in the_enum:
                combobox.addItem(member.value, member)

        # 连接信号和槽，当用户选择一个选项时触发
        combobox.currentIndexChanged.connect(
            lambda: self._on_combobox_changed_(combobox=combobox,
                                               key_path=key_path,
                                               default_value=default_value,
                                               func_set_config=func_set_config)
        )

    def _on_combobox_changed_(self,
                              combobox: QComboBox,
                              key_path: Optional[List[str]] = None,
                              default_value: Any = None,
                              func_set_config: Optional[Callable] = None) -> None:
        """
        处理下拉框变化事件，更新配置字典。

        Args:
            combobox (QComboBox): QComboBox实例，其当前数据作为要设置的值。
            key_path (Optional[List[str]]): 配置字典中的键路径。
            default_value (Any): 如果键路径不存在，则使用的默认值。
            func_set_config (Optional[Callable]): 设置配置的函数。
        """
        selected_value = combobox.currentData()  # 获取下拉框当前选中的枚举值
        if func_set_config:
            func_set_config(selected_value)
        else:
            ConfigTool.reset_config_attr(config_dict=self.config_args,
                                         key_path=key_path,
                                         the_value=selected_value.value if selected_value else default_value)
