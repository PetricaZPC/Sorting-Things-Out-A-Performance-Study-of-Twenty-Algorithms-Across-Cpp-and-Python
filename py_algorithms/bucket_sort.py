from __future__ import annotations

from typing import Any
from .common import _copy


def bucket_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if not a:
        return a
    if not all(isinstance(value, (int, float)) for value in a):
        return sorted(a)
    min_val = min(a)
    max_val = max(a)
    if min_val == max_val:
        return a
    n = len(a)
    buckets: list[list[Any]] = [[] for _ in range(n)]
    range_span = float(max_val - min_val)
    for value in a:
        index = int((value - min_val) / range_span * (n - 1))
        buckets[index].append(value)
    result: list[Any] = []
    for bucket in buckets:
        result.extend(sorted(bucket))
    return result
