from __future__ import annotations

from typing import Any
from .common import _copy


def comb_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    gap = len(a)
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        for i in range(len(a) - gap):
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]
                sorted_flag = False
    return a
