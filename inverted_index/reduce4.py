#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math

def reduce_one_group(key, group, total_docs):
    locations = []
    # keyword = ""
    group_len = 0
    for line in group:
        #print(line)
        words = line.split()
        keyword = words[0]
        doc_score = words[1]
        locations.append(words[2] + " " + words[3] + " " + words[4])
        group_len += 1
    #print(f"{key} {word_count}")
    print(keyword + " " + doc_score, end = " ")
    print(*locations)
  
    #print("\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #print("partition: " + line.partition("\t")[0])
    keyword = line.partition(" ")[0]
    return keyword

def main():
    """Divide sorted lines into groups that share a key."""
    i = 0
    f = open("output1/total_document_count.txt", "r")
    total_docs = int(f.readline())
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group, total_docs)
        # print(i)
        i += 1


if __name__ == "__main__":
    main()
