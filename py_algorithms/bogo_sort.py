from __future__ import annotations

import random
from typing import Any
from .common import _copy, is_sorted


def bogo_sort(arr: list[Any]) -> list[Any]:
    a = _copy(arr)
    max_attempts = 10_000
    attempts = 0
    while not is_sorted(a) and attempts < max_attempts:
        random.shuffle(a)
        attempts += 1
    return a
