#!/usr/bin/env python3
"""Reduce 0."""

import sys
import itertools

# sums and outputs number of lines
def reduce0(key, group):
    group = list(group)
    total = 0
    for line in group:
        total += 1

    print(f"{total}")


def main():
    """Divide sorted lines into groups that share a key.
    Docs: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    groups = itertools.groupby(sys.stdin, lambda x: x.partition("\t")[0])
    for key, group in groups:
        reduce0(key, group)


if __name__ == "__main__":
    main()