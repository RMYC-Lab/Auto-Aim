"""Parameter checker"""
from typing import Any
from enum import EnumMeta


class CheckerBase:
    """
    Checker base class
    检查参数类型 基类
    """
    def __init__(self):
        ...

    def check(self, value: Any) -> bool:
        """
        Check value
        检查值
        """
        raise NotImplementedError

    def format(self, value: Any) -> str:
        """
        Format value
        格式化值
        """
        raise NotImplementedError

    # 或运算
    def __or__(self, other: 'CheckerBase') -> 'CheckerSet':
        return CheckerSet(self, other)


class CheckerSet(CheckerBase):
    """
    Checker set
    检查器集合
    """
    def __init__(self, *checkers: CheckerBase):
        self.checkers = list()
        for checker in checkers:
            if isinstance(checker, CheckerSet):
                self.checkers += checker.checkers
                continue
            assert isinstance(checker, CheckerBase), f"Invalid checker: {checker}"
            self.checkers.append(checker)

    def check(self, value: Any) -> bool:
        return any(checker.check(value) for checker in self.checkers)

    def format(self, value: Any) -> str:
        for checker in self.checkers:
            if checker.check(value):
                return checker.format(value)
        assert False, "No checker matched"


class EmptyChecker(CheckerBase):
    """
    Empty checker
    空检查
    """
    def check(self, value: Any) -> bool:
        return True

    def format(self, value: Any) -> str:
        return value


class IntChecker(CheckerBase):
    """
    Integer checker
    整数检查
    """

    MAX_INT = 2**31 - 1
    MIN_INT = -2**31

    def __init__(self, min: int = MIN_INT, max: int = MAX_INT):
        self.max = max
        self.min = min

    def check(self, value: int) -> bool:
        return isinstance(value, int) and self.min <= value <= self.max

    def format(self, value: int) -> str:
        assert self.check(value), f"Invalid integer: {value}"
        return str(int(value))


class FloatChecker(CheckerBase):
    """
    Float checker
    小数检查
    """

    MAX_DECIMAL = 2**31 - 1
    MIN_DECIMAL = -2**31
    PRECISION = 3

    def __init__(self, min: float = MIN_DECIMAL, max: float = MAX_DECIMAL, precision: int = PRECISION):
        self.min = min
        self.max = max
        self.precision = precision

    def check(self, value: float) -> bool:
        return (isinstance(value, int) or isinstance(value, float)) and self.min <= value <= self.max

    def format(self, value: float) -> str:
        assert self.check(value), f"Invalid decimal: {value}"
        return format(value, f'.{self.precision}f')


class EnumChecker(CheckerBase):
    """
    Enum checker
    枚举检查
    """

    def __init__(self, enum: EnumMeta):
        self.enum = enum

    def check(self, value: Any) -> bool:
        return value in self.enum and isinstance(value, type(self.enum))

    def format(self, value: Any) -> str:
        assert self.check(value), f"Invalid enum: {value}"
        return str(value)
