# /usr/bin/env python3
""" Solution (prototype?) for day 5 of advent of code
https://adventofcode.com/2023/day/5
"""

from tqdm import tqdm
from loguru import logger


def map_lookup(
    start_num: int, destinations: list[int], sources: list[int], rngs: list[int]
) -> int:
    """Perform a lookup for a single almanac entry"""
    # assumption: overlaps in sources cannot exist
    destination: int = -1
    # optim: compute across all dst/src/rng simultaneously. Result is any non-start
    for _dst, _src, _rng in zip(destinations, sources, rngs):
        logger.debug(f"Testing {start_num} against ({_dst} {_src} {_rng})")
        # first handle trivial cases: start_num cannot exist in range
        if start_num < _src:
            logger.debug(f"{start_num} < {_src}")
            # will be overwritten if a subsequent source includes it
            destination = start_num
            continue

        elif start_num > _src + _rng:
            destination = start_num
            logger.debug(f"{start_num} > {_src} + {_rng} ({_src + _rng})")
            continue  # nothing to see here; skip

        # if here, start_num _must_ be in range
        destination = _dst + (start_num - _src)
        logger.debug(f"{destination} = {_dst} + {start_num} - {_src}")
        break  # exist once a single valid conversion exists (only one *can*)

    assert destination > 0, "No destination found!"

    return destination


def examine_seed(
    seed_num: int,
    destinations: list[list[int]],
    sources: list[list[int]],
    ranges: list[list[int]],
) -> int:
    """Fully processes a single seed"""
    val = seed_num
    for _dsts, _srcs, _rngs in zip(destinations, sources, ranges):
        val = map_lookup(val, _dsts, _srcs, _rngs)
        logger.debug(f"Mapped to {val}")

    return val


test_destinations = [
    [50, 52],
    [0, 37, 39],
    [49, 0, 42, 57],
    [88, 18],
    [45, 81, 68],
    [0, 1],
    [60, 56],
]
test_sources = [
    [98, 50],
    [15, 52, 0],
    [53, 11, 0, 7],
    [18, 25],
    [77, 45, 64],
    [69, 0],
    [56, 93],
]
test_ranges = [
    [2, 48],
    [37, 2, 15],
    [8, 42, 7, 4],
    [7, 70],
    [23, 19, 13],
    [1, 69],
    [37, 4],
]
