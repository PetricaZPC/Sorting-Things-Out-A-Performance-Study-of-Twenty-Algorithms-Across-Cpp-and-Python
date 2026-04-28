from __future__ import annotations

from typing import Any
from .common import _copy


def insertion_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
