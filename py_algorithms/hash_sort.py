from __future__ import annotations

from typing import Any
from .common import _copy


def hash_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    if not a:
        return a
    counter: dict[Any, int] = {}
    for value in a:
        counter[value] = counter.get(value, 0) + 1
    result: list[Any] = []
    for key in sorted(counter):
        result.extend([key] * counter[key])
    return result
