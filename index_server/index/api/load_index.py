import flask
import index
from index import app
from pathlib import Path
import os

keywords = {}

@index.app.route('/api/v1/', methods=["GET"])
def services_list():
    context = {"hits": "/api/v1/hits/", "url": "/api/v1/"}
    return flask.jsonify(**context), 200


@index.app.route('/api/v1/hits/', methods=["GET"])
def hit_list():
    hlist = []
    doc_list = []
    query_string = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0, type=float)
    queries = query_string.split("+")
    print(queries)
    for query in queries:
        doc_list.append({})
        line = keywords[query]
        for i in line[1:]:
            if i % 3 == 0:
                doc_list[-1][line[i]] = (line[i + 1], line[i + 2])
    #find intersecting keys
    context = {"hits": hlist}
    return flask.jsonify(**context), 200

def load_index():
    #stopwords_file = open("stopwords.txt", "r")
    #stopwords = stopwords_file.read()
    #stopwords = stopwords.replace('\n', ' ').split()
    
    print(os.getcwd())
    print( os.listdir())
    os.chdir('index_server/index/') 
    idx_file = app.config["INDEX_PATH"]
    print(idx_file)
    index_file = open("inverted_index/" + idx_file, "r")
    stopwords_file = open("stopwords.txt", "r")
    pagerank_file = open("pagerank.out", "r")
    stopwords = stopwords_file.read()
    pagerank = pagerank_file.read()
    index_lines = index_file.readlines()
    stopwords = stopwords.replace('\n', ' ').split()
    #print(stopwords)
    for line in index_lines:
        terms = line.split()
        keywords[terms[0]] = terms[1:]
    print(keywords)
    print("henslo")