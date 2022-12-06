#!/usr/bin/env python3
"""Word count mapper."""
import sys
import csv
import re

def main():
    for line in sys.stdin:
        print(line.rstrip())
    
if __name__ == "__main__":
    main()