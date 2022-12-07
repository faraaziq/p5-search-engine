#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math

def reduce_one_group(key, group, total_docs):
    temp_normfactor = 0
    line_list = []
    # keyword = ""
    for l in group:
        #print(line)
        words = l.split()
        line_list.append(l)
        temp_normfactor += ((float(words[2]) * float(words[3]))**2)
    #print(f"{key} {word_count}")
    for line in line_list:
        print(line.rstrip() + " " + str(temp_normfactor))


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #print("partition: " + line.partition("\t")[0])
    keyword = line.partition(" ")[0]
    return keyword

def inverse_doc_score(total_docs, docs_with_term):
    return math.log10(total_docs / docs_with_term)

def normalization_factor(term_freq_in_doc, inverse_doc_score):
    n = (term_freq_in_doc * inverse_doc_score) ** 2
    return n

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
