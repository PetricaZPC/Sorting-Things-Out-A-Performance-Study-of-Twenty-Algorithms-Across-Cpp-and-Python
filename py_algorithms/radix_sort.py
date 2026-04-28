from __future__ import annotations

from typing import Any
from .common import _copy


def radix_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if not a:
        return a
    if all(isinstance(x, int) for x in a):
        if any(x < 0 for x in a):
            offset = -min(a)
            a = [x + offset for x in a]
        else:
            offset = 0
        max_val = max(a)
        exp = 1
        while max_val // exp > 0:
            buckets = [[] for _ in range(10)]
            for value in a:
                buckets[(value // exp) % 10].append(value)
            a = [num for bucket in buckets for num in bucket]
            exp *= 10
        if offset:
            a = [x - offset for x in a]
        return a
    if all(isinstance(x, str) for x in a):
        max_len = max(len(x) for x in a)
        for pos in range(max_len - 1, -1, -1):
            buckets = [[] for _ in range(257)]
            for s in a:
                index = ord(s[pos]) + 1 if pos < len(s) else 0
                buckets[index].append(s)
            a = [item for bucket in buckets for item in bucket]
        return a
    return sorted(a)
