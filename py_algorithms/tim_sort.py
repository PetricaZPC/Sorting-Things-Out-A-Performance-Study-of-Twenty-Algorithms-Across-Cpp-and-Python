from __future__ import annotations

from typing import Any
from .common import _copy


def tim_sort(arr: list[Any]) -> list[Any]:
    return sorted(_copy(arr))
