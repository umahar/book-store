"""
Exercism solution for "book-store"
"""

import math
from collections import Counter
from decimal import Decimal
from functools import lru_cache, reduce
from typing import List, Tuple

PER_BOOK = Decimal("800.00")
PER_GROUP = {
    1: 1 * PER_BOOK * Decimal("1.00"),
    2: 2 * PER_BOOK * Decimal("0.95"),
    3: 3 * PER_BOOK * Decimal("0.90"),
    4: 4 * PER_BOOK * Decimal("0.80"),
    5: 5 * PER_BOOK * Decimal("0.75"),
}


# memoize the results; cap memory and degrade performance with HUGE number of books
@lru_cache(maxsize=1024)
def _recursive_total(books: Tuple[int]) -> float:
    """
    Recurse to find the best discounted price for a non-empty, pre-sorted tuple of books.
    """
    volumes = Counter(books)
    num_books, num_volumes = len(books), len(volumes)

    # optimization 1: we only have N copies of the same volume
    if num_volumes == 1:
        return num_books * PER_BOOK

    # optimization 2: we only have 1 copy of each unique volume
    if num_books == num_volumes:
        return PER_GROUP[num_books]

    # optimization 3: we happen to have gotten counts that share a GCD > 1
    gcd = reduce(math.gcd, volumes.values())
    if gcd != 1:
        minimal = Counter({k: v // gcd for k, v in volumes.items()})
        minimal_books = tuple(sorted(minimal.elements()))
        return _recursive_total(minimal_books) * gcd

    # in all other cases we recurse into the groups to find the minimum discount
    price = num_books * PER_BOOK
    for num in range(num_volumes, 1, -1):
        # remove the first copy of each of the num most common volumes
        group = volumes - Counter(k for k, _ in volumes.most_common(num))
        group_books = tuple(sorted(group.elements()))
        # calculate the minimum price for the group
        price = min(price, PER_GROUP[num] + _recursive_total(group_books))
    return price


def total(books: List[int]) -> float:
    """
    Calculate the best discounted price for a list of books.
    """
    if not books:
        return 0
    return _recursive_total(tuple(sorted(books)))
