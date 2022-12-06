"""Index Server REST API."""

import os

STOP_WORDS = []
PAGE_RANK = {}
INVERTED_INDEX = {}
DOC_LIST = {}

def load_index():

    file_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(file_dir, 'stopwords.txt')

    file1 = open(file_path, 'r')
    for line in file1:
        STOP_WORDS.append(line)
    file1.close()

    file_path = os.path.join(file_dir, 'pagerank.out')
    file2 = open(file_path, 'r')
    for line in file2:
        slices = line.split(",")
        PAGE_RANK[slices[0]] = slices[1]
    file2.close()

    file_path = os.path.join(file_dir, 'inverted_index/part-00000')
    file3 = open(file_path, 'r')
    for line in file3:
        data_list = []
        docs_list = []

        #splits each line of inverted index into 'items'
        #complies data for each doc as list of tuples 'data list'
        items = line.split()
        length = len(items)
        for x in range(2, length, 3):
            term_data = (items[x], items[x+1], items[x+2])
            data_list.append(term_data)
            docs_list.append(items[x])
        INVERTED_INDEX[items[0]] = (items[1], data_list)
        DOC_LIST[items[0]] = docs_list
    file3.close()

from index.api.main import get_url
from index.api.main import get_hits