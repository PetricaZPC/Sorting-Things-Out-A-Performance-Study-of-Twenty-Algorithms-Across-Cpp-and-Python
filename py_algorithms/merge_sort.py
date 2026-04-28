from __future__ import annotations

from typing import Any
from .common import _copy, _parallel_merge_sort


def merge_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    return _parallel_merge_sort(a)
