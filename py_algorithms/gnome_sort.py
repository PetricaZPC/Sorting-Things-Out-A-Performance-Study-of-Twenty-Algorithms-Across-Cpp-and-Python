from __future__ import annotations

from typing import Any
from .common import _copy


def gnome_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    i = 1
    while i < len(a):
        if a[i] >= a[i - 1]:
            i += 1
        else:
            a[i], a[i - 1] = a[i - 1], a[i]
            i = max(i - 1, 1)
    return a
