# /usr/bin/env python3
""" Solution (prototype?) for day 5 of advent of code
https://adventofcode.com/2023/day/5
"""

from functools import partial
from tqdm import tqdm
from loguru import logger
import numpy as np


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
    destinations: list[list[int]],
    sources: list[list[int]],
    ranges: list[list[int]],
    seed_num: int,
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


if __name__ == "__main__":
    with open("input.txt") as in_f:
        seeds = list(map(int, in_f.readline().strip().split(": ")[-1].split(" ")))
        logger.debug(f"{seeds}")

        in_dsts = []
        in_srcs = []
        in_rngs = []

        tmp = in_f.readline()  # skip blank line and header
        logger.debug(tmp)

        map_idx = 0
        reached_end = False
        while not reached_end:
            in_dsts.append([])
            in_srcs.append([])
            in_rngs.append([])

            in_f.readline()  # skip header
            while (n_line := in_f.readline()) != "\n":
                if n_line == "":  # eof, quit
                    reached_end = True
                    break
                _dst, _src, _rng = n_line.strip().split(" ")
                logger.debug(f"Read {_dst}, {_src}, {_rng}")
                in_dsts[map_idx].append(int(_dst))
                in_srcs[map_idx].append(int(_src))
                in_rngs[map_idx].append(int(_rng))

            map_idx += 1

            logger.debug(f"dsts {in_dsts}")
            logger.debug(f"srcs {in_srcs}")
            logger.debug(f"rngs {in_rngs}")

    examine_f = partial(examine_seed, in_dsts, in_srcs, in_rngs)
    locations = np.fromiter(map(examine_f, seeds), dtype=int)
