from __future__ import annotations

import heapq
from typing import Any
from .common import _copy


def heap_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]
