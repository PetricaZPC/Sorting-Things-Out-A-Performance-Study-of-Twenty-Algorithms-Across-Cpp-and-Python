from __future__ import annotations

from typing import Any
from .common import _copy


def counting_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if not a:
        return a
    if not all(isinstance(x, int) for x in a):
        return sorted(a)
    min_val = min(a)
    max_val = max(a)
    span = max_val - min_val
    if span < 0:
        return sorted(a)
    if span > 10_000_000:
        return sorted(a)
    count = [0] * (span + 1)
    for value in a:
        count[value - min_val] += 1
    result: list[int] = []
    for offset, freq in enumerate(count):
        result.extend([offset + min_val] * freq)
    return result
