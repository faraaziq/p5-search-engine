#!/usr/bin/env python3
"""Word count mapper."""
import sys
import csv
import re

def main():
    stopwords_file = open("stopwords.txt", "r")
    stopwords = stopwords_file.read()
    stopwords = stopwords.replace('\n', ' ').split()
    for line in sys.stdin:
        words = (line.partition(",")[2].partition(",")[2].strip('"'))
        words = re.sub(r"[^a-zA-Z0-9 ]+", "", words)
        words = words.split()
        doc_num = line.partition(",")[0].strip('"')
        for word in words:
            # print(doc_num)
            if word.casefold() not in stopwords:
                print(f"{word.casefold()} {doc_num} 1")
    
if __name__ == "__main__":
    main()