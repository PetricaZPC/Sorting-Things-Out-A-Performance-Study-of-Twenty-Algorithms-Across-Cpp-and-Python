from __future__ import annotations

import gc
import random
from concurrent.futures import ProcessPoolExecutor
from typing import Any

PARALLEL_THRESHOLD = 20000


def _copy(arr: list[Any]) -> list[Any]:
    return list(arr)


def is_sorted(arr: list[Any]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def _merge_sorted(left: list[Any], right: list[Any]) -> list[Any]:
    merged: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def _sequential_merge_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = _sequential_merge_sort(arr[:mid])
    right = _sequential_merge_sort(arr[mid:])
    return _merge_sorted(left, right)


def _parallel_merge_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= PARALLEL_THRESHOLD:
        return _sequential_merge_sort(arr)
    mid = len(arr) // 2
    with ProcessPoolExecutor() as executor:
        left_future = executor.submit(_parallel_merge_sort, arr[:mid])
        right = _parallel_merge_sort(arr[mid:])
        left = left_future.result()
    return _merge_sorted(left, right)


def _sequential_quick_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return _sequential_quick_sort(left) + middle + _sequential_quick_sort(right)


def _parallel_quick_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= PARALLEL_THRESHOLD:
        return _sequential_quick_sort(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    with ProcessPoolExecutor() as executor:
        left_future = executor.submit(_parallel_quick_sort, left)
        right_future = executor.submit(_parallel_quick_sort, right)
        left_sorted = left_future.result()
        right_sorted = right_future.result()
    return left_sorted + middle + right_sorted


def cleanup() -> None:
    gc.collect()
