#!/usr/bin/env python3
"""Word count mapper."""
import sys
import csv
import re

def main():
    for line in sys.stdin:
        line = line[0:csv.field_size_limit(sys.maxsize)]
        doc_num = line.partition(",")[0].strip('"')
        # print(doc_num)
        print(f"1\t{doc_num}")
    
if __name__ == "__main__":
    main()