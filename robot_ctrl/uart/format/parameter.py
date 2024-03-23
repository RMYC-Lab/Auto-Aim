"""Parameter for UART protocol."""

from typing import Any
from enum import Enum

from .checker import CheckerBase, EmptyChecker

USE_DEFAULT = object()


class ParamType(Enum):
    """
    Parameter Type
    参数类型
    """
    value_only = "value_only"           # 只有值
    value_and_key = "value_and_key"
    key_only = "key_only"


class Parameter:
    """Parameter class"""
    def __init__(self, key: str, default_value: Any = None,
                 checker: CheckerBase = EmptyChecker(),
                 param_type: ParamType = ParamType.value_only):
        self.key = key
        self.default_value = default_value
        self.checker = checker
        self.param_type = param_type

    def check(self, value: Any = USE_DEFAULT) -> bool:
        """
        Check parameter
        检查参数
        """
        if value is USE_DEFAULT:
            value = self.default_value
        return self.checker.check(value)

    def format(self, value: Any = USE_DEFAULT) -> str:
        """
        Format parameter
        格式化参数
        """
        if value is USE_DEFAULT:
            value = self.default_value
        assert self.check(value)
        format_value = self.checker.format(value)
        if self.param_type == ParamType.value_only:
            return f" {format_value}"
        elif self.param_type == ParamType.value_and_key:
            return f" {self.key} {format_value}"
        elif self.param_type == ParamType.key_only:
            return f" {self.key}"
        else:
            assert False, "Unknown parameter type"
