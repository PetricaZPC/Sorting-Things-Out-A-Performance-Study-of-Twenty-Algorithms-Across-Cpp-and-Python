from __future__ import annotations

from typing import Any
from .common import _copy


def pancake_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    n = len(a)
    for size in range(n, 1, -1):
        max_idx = max(range(size), key=lambda i: a[i])
        if max_idx != size - 1:
            a[: max_idx + 1] = reversed(a[: max_idx + 1])
            a[:size] = reversed(a[:size])
    return a
