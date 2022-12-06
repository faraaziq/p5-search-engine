#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    word_count = 0
    keywords = []
    for line in group:
        #print(line)
        keywords = line.split()
        word_count += int(keywords[2])
    #print(f"{key} {word_count}")
    print(keywords[0] + " " + keywords[1] + " " + str(word_count))
    return word_count


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #print("partition: " + line.partition("\t")[0])
    keyword = line.partition(" ")[0]
    doc_id = line.partition(" ")[2].partition(" ")[0]
    return keyword + " " + doc_id


def main():
    """Divide sorted lines into groups that share a key."""
    i = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
        # print(i)
        i += 1


if __name__ == "__main__":
    main()
