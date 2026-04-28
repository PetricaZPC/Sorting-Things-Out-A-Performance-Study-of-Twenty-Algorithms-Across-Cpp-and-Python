from .bitonic_sort import bitonic_sort
from .bubble_sort import bubble_sort
from .bucket_sort import bucket_sort
from .cocktail_shaker_sort import cocktail_shaker_sort
from .comb_sort import comb_sort
from .counting_sort import counting_sort
from .gnome_sort import gnome_sort
from .hash_sort import hash_sort
from .heap_sort import heap_sort
from .insertion_sort import insertion_sort
from .merge_sort import merge_sort
from .odd_even_sort import odd_even_sort
from .pancake_sort import pancake_sort
from .pigeonhole_sort import pigeonhole_sort
from .quick_sort import quick_sort
from .radix_sort import radix_sort
from .selection_sort import selection_sort
from .shell_sort import shell_sort
from .stooge_sort import stooge_sort
from .tim_sort import tim_sort

SORT_ALGORITHMS = {
    "bitonic_sort": bitonic_sort,
    "bubble_sort": bubble_sort,
    "bucket_sort": bucket_sort,
    "cocktail_shaker_sort": cocktail_shaker_sort,
    "comb_sort": comb_sort,
    "counting_sort": counting_sort,
    "gnome_sort": gnome_sort,
    "hash_sort": hash_sort,
    "heap_sort": heap_sort,
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
    "odd_even_sort": odd_even_sort,
    "pancake_sort": pancake_sort,
    "pigeonhole_sort": pigeonhole_sort,
    "quick_sort": quick_sort,
    "radix_sort": radix_sort,
    "selection_sort": selection_sort,
    "shell_sort": shell_sort,
    "stooge_sort": stooge_sort,
    "tim_sort": tim_sort,
}

ALL_SORTS = list(SORT_ALGORITHMS.keys())


def get_algorithm_names() -> list[str]:
    return ALL_SORTS
