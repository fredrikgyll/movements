from __future__ import annotations

from enum import Enum, EnumMeta
from typing import Any


class MetaEnum(EnumMeta):
    """
    Overwrites __contains__ so we can do `"string" in Enum`.
    """

    def __contains__(cls, item: Any) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    @classmethod
    def choices(cls) -> list:
        return list(cls)


class StrEnum(str, BaseEnum):
    def __str__(self) -> str:
        return self.value


class IntEnum(int, BaseEnum):
    def __str__(self) -> str:
        return str(self.value)
