from __future__ import annotations

from typing import Any
from .common import _copy


def pigeonhole_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if not a or not all(isinstance(x, int) for x in a):
        return sorted(a)
    min_val = min(a)
    max_val = max(a)
    size = max_val - min_val + 1
    if size > 1_000_000:
        return sorted(a)
    holes: list[list[int]] = [[] for _ in range(size)]
    for value in a:
        holes[value - min_val].append(value)
    result: list[int] = []
    for hole in holes:
        result.extend(hole)
    return result
