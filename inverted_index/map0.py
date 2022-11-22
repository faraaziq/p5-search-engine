#!/usr/bin/env python3
"""Map 0."""

import sys
import csv
import re

csv.field_size_limit(sys.maxsize)

for row in csv.reader(sys.stdin):
    #outputs doc, 1 for each line
    print(f"doc\t1")