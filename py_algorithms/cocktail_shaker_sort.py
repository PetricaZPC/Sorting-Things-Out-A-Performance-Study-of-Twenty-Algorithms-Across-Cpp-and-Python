from __future__ import annotations

from typing import Any
from .common import _copy


def cocktail_shaker_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    left, right = 0, n - 1
    while left < right:
        for i in range(left, right):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
        right -= 1
        for i in range(right, left, -1):
            if a[i - 1] > a[i]:
                a[i], a[i - 1] = a[i - 1], a[i]
        left += 1
    return a
