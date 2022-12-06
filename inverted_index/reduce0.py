#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    word_count = 0
    for line in group:
        #print(line)
        count = line.partition("\t")[0]
        word_count += int(count)
    #print(f"{key} {word_count}")
    return word_count


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #print("partition: " + line.partition("\t")[0])
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    total_doc_count = 0
    i = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        total_doc_count += reduce_one_group(key, group)
        #print(i)
        i += 1
    print(total_doc_count)


if __name__ == "__main__":
    main()
