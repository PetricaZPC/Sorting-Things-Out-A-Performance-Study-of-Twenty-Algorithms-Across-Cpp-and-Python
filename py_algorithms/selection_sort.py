from __future__ import annotations

from typing import Any
from .common import _copy


def selection_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a
