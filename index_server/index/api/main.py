"""REST API for main."""

import index
import flask
from flask import request
import math
import re
import os

STOP_WORDS = []
PAGE_RANK = {}
INVERTED_INDEX = {}
DOC_LIST = {}
file_dir = ""
def load_index():
    global STOP_WORDS
    global file_dir
    file_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(file_dir, 'stopwords.txt')

    file1 = open(file_path, 'r')
    #for line in file1:
    stopwords = file1.read()
    STOP_WORDS = stopwords.replace('\n', ' ').split()
    #print(STOP_WORDS)
        #STOP_WORDS.append(line)
    file1.close()

    file_path = os.path.join(file_dir, 'pagerank.out')
    file2 = open(file_path, 'r')
    for line in file2:
        slices = line.split(",")
        PAGE_RANK[slices[0]] = float(slices[1])
    file2.close()

    
    index_path = "inverted_index/"
    index_path += index.app.config["INDEX_PATH"]
    file_path = os.path.join(file_dir, index_path)
    file_dir = os.path.join(file_dir, "inverted_index/")
    file3 = open(file_path, 'r')
    for line in file3:
        data_list = []
        docs_list = []

        #splits each line of inverted index into 'items'
        #complies data for each doc as list of tuples 'data list'
        items = line.split()
        length = len(items)
        for x in range(2, length, 3):
            term_data = (items[x], int(items[x+1]), float(items[x+2]))
            data_list.append(term_data)
            docs_list.append(items[x])
        INVERTED_INDEX[items[0]] = (float(items[1]), data_list)
        DOC_LIST[items[0]] = docs_list
    file3.close()
    file_dir = os.listdir(file_dir)

def get_TFIDF(q, d, norm_d):
   dot_product = 0
   norm_q_square = 0

   length = len(q)
   for i in range(0, length):
       dot_product += (q[i] * d[i])
       norm_q_square += (q[i] * q[i])

   norm_q = math.sqrt(norm_q_square)
   norms = (norm_q * norm_d)
   tfidf_score = (dot_product / norms)

   return tfidf_score

@index.app.route("/api/v1/")
def get_url():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    
    return flask.jsonify(**context)

@index.app.route("/api/v1/hits/")
def get_hits():
    #set query variables from arguments
    args = request.args
    weight = args.get('w', default=0.5, type=int)
    queries = args.get('q').split(' ')
    #print(dirty_queries)
    queries = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in queries]

    #gets set of docs containing all queries and dict of term frequency
    freq_map = {}
    docs_list = []
    
    global STOP_WORDS
   

    for query in queries:
        if query not in STOP_WORDS:
           
            
            if query in freq_map.keys():
                freq_map[query] += 1
            else:
                freq_map[query] = 1

            if query in DOC_LIST.keys():
                tmp_set = set(DOC_LIST[query])
                docs_list.append(tmp_set)
       # else:
           # queries.remove(query)
    
    print("docslist: ")
    hits = []
    #hits.append({"docid": 0, "score": 0})
    print(docs_list)
    if docs_list:
        docs = set.intersection(*docs_list)
    else:
        
        return flask.jsonify({"hits": file_dir}), 200
        
    #searches inverted index and builds q and d vectors and dict of doc norms
    q_vector = []
    d_vector = []
    doc_norms = {}

    for query in queries:
        if query not in STOP_WORDS:
            idf = INVERTED_INDEX[query][0]
            items = INVERTED_INDEX[query][1]
            for item in items:
                if item[0] in docs:
                    
                    q_vector.append(freq_map[query] * float(idf))
                    d_vector.append(item[1] * float(idf))
                    doc_norms[item[0]] = item[2]

   
    #get score for each doc
    results = []

    for doc in docs:
        norm_d = doc_norms[doc]
        tfidf = get_TFIDF(q_vector, d_vector, norm_d)
        doc_score = (weight * PAGE_RANK[doc])
        doc_score += ((1 - weight) * tfidf)
        results.append((doc, doc_score))
    results = sorted(results, key=lambda x: x[1], reverse=True)

    #return results in json format
    
    for result in results:
        hits.append({"docid": result[0], "score": result[1]})

  
    return flask.jsonify({"hits": hits}), 200