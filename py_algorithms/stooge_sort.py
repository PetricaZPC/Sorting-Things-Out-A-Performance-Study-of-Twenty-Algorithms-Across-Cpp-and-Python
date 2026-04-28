from __future__ import annotations

from typing import Any
from .common import _copy


def stooge_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    if n <= 1:
        return a
    if a[0] > a[-1]:
        a[0], a[-1] = a[-1], a[0]
    if n > 2:
        t = n // 3
        a[: n - t] = stooge_sort(a[: n - t])
        a[t:] = stooge_sort(a[t:])
        a[: n - t] = stooge_sort(a[: n - t])
    return a
