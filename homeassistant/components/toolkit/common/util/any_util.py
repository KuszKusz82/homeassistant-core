from typing import Any


class AnyUtil:
    @staticmethod
    def as_int(value: Any) -> int:
        if value is not None:
            return int(value)
        raise ValueError("Value should not be None")

    @staticmethod
    def as_list(value: Any) -> list:
        if value is not None:
            return list(value)
        raise ValueError("Value should not be None")

    @staticmethod
    def as_str(value: Any) -> str:
        if value is not None:
            return str(value)
        raise ValueError("Value should not be None")


as_list = AnyUtil.as_list
as_int = AnyUtil.as_int
as_str = AnyUtil.as_str
