from __future__ import annotations

from typing import Any
from .common import _copy


def shell_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a
