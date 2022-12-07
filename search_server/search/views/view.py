"""ask485 index view."""

import requests
import os
import heapq
import threading
import time
import json
import flask
from flask import request
import search

search_res = []

def request_api(url, query):
    response = requests.get(url, params=query)
    res_data = response.json()
    for res_datum in res_data["hits"]:
        search_res.append((res_datum["docid"], res_datum["score"]))

@search.app.route("/", methods=["GET"])
def show_index():
    args = request.args
    weight = args.get('w', default=0.5, type=int)
    query = args.get('q')

    if query is None:
        return flask.render_template("index.html")
    
    #initialize variables for API calls
    params = {'q': query, 'w': weight}
    urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']
    threads = []
    hitlist = []
    docs = []

    #start threads
    for url in urls:
        thread = threading.Thread(target=request_api, args=(url,params))
        threads.append(thread)
        thread.start()

    #join threads
    for t in threads:
        t.join()

    #merge lists
    #hits_list = list(heapq.merge(*search_res, key=lambda x: x[1], reverse=True))

    hitlist = sorted(search_res,key=lambda x: x[1], reverse=True)

    search_range = 10
    if len(hitlist) < 10:
        search_range = len(hitlist)  

    ids = []
    for i in range(0,search_range):
        ids.append(hitlist[i][0])

    connection = search.model.get_db()
    cur = connection.execute(
        "SELECT title, summary, url FROM Documents WHERE docid = ?", id)
    results = cur.fetchall()

    context = {"results": results}
    return flask.render_template("index.html", **context)
   