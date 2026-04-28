from __future__ import annotations

from typing import Any
from .common import _copy


def odd_even_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        for i in range(1, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
        for i in range(0, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
    return a
