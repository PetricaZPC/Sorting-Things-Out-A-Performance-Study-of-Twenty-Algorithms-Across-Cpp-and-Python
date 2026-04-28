from __future__ import annotations

from typing import Any
from .common import _copy


def bubble_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a
