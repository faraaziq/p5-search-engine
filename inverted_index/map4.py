#!/usr/bin/env python3
"""Word count mapper."""
import sys
import csv
import re

def main():
    for line in sys.stdin:
        words = line.split()
        tmp = words[0]
        words[0] = words[1]
        words[1] = tmp

        tmp = words[3]
        words[3] = words[1]
        words[1] = tmp
        
        tmp = words[3]
        words[3] = words[2]
        words[2] = tmp
        print(*words)
    
if __name__ == "__main__":
    main()