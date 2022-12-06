"""REST API for main."""

import index
import flask
import math
import re

def clean(words):
    for word in words:
        word = re.sub(r"[^a-zA-Z0-9 ]+", "", word)
        word = word.casefold()
    new_words = [x for x in words if x not in STOP_WORDS]
    return new_words

def get_TFIDF(q, d, norm_d):
   dot_product = 0
   norm_q_square = 0

   length = len(q)
   for i in range(0, length):
       dot_product += (q[i] * d[i])
       norm_q_square += (q[i] * q[i])

   norm_q = sqrt(norm_q_square)
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
    dirty_queries = args.get('q').split('+')
    queries = clean(dirty_queries)

    #gets set of docs containing all queries and dict of term frequency
    freq_map = {}
    docs_list = []
    
    for query in queries:
        freq_map[query] += 1
        tmp_set = set(DOC_LIST[query])
        docs_list.append(tmp_set)
    docs = set.intersection(*docs_list)

    #searches inverted index and builds q and d vectors and dict of doc norms
    q_vector = []
    d_vector = []
    doc_norms = {}

    for query in queries:
        idf = INVERTED_INDEX[query][0]
        items = INVERTED_INDEX[query][1]
        for item in items:
            if item[0] in docs:
                q_vector.append(freq_map[query] * idf)
                d_vector.append(item[1] * idf)
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
    hits = []
    for result in results:
        hits.append({"docid": result[0], "score": result[1]})

    return \
        flask.jsonify({"hits": hits})