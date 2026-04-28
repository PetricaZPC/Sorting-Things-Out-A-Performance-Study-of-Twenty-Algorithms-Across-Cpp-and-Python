from __future__ import annotations

from typing import Any
from .common import _copy, _parallel_quick_sort


def quick_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    return _parallel_quick_sort(a)
