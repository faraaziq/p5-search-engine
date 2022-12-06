"""ask485 index view."""

import requests
import os
import heapq
import threading
import time
import json
import flask
import search

search_res = []

def request_api(url, query):
    response = requests.get(url, params=query)
    res_data = json.loads(response.json())
    search_res.append(res_data['hits'])

@search.app.route("/", methods=["GET"])
def show_index():
    args = request.args
    weight = args.get('w', default=0.5, type=int)
    query = args.get('q')

    if query is None:
        return flask.render_template("index.html")
    
    #initialize variables for API calls
    params = {'q': query, 'w': weight}
    urls = search.app.config[SEARCH_INDEX_SEGMENT_API_URLS]
    threads = []

    #start threads
    for url in urls:
        thread = threading.Thread(target=request_api, args=(url,params))
        threads.append(thread)
        thread.start()

    #join threads
    for t in threads:
        t.join()

    #merge lists
    hits_list = heapq.merge(*search_res, key=lambda x: x[1], reverse=True)

    hits_size = len(hits_list)
    if hits_size < 10:
        search_range = hits_size

    res_docs = []
    for i in range(0,search_range):
        res_docs.append(hits[i][0])


    connection = search.model.get_db()
    cur = connection.execute(
        "SELECT title, summary, url "
        "FROM Documents "
        "WHERE username1 = ? ", (flask.session["username"],))