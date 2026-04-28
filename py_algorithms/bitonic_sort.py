from __future__ import annotations

from typing import Any
from .common import _copy


def bitonic_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if len(a) <= 1:
        return a
    n = 1 << (len(a) - 1).bit_length()
    sentinel = max(a)
    a.extend([sentinel] * (n - len(a)))

    def compare_and_swap(data: list[Any], i: int, j: int, direction: bool) -> None:
        if direction == (data[i] > data[j]):
            data[i], data[j] = data[j], data[i]

    def bitonic_merge(data: list[Any], low: int, cnt: int, direction: bool) -> None:
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(data, i, i + k, direction)
            bitonic_merge(data, low, k, direction)
            bitonic_merge(data, low + k, k, direction)

    def bitonic_sort_inner(data: list[Any], low: int, cnt: int, direction: bool) -> None:
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_inner(data, low, k, True)
            bitonic_sort_inner(data, low + k, k, False)
            bitonic_merge(data, low, cnt, direction)

    bitonic_sort_inner(a, 0, n, True)
    return a[: len(arr)]
