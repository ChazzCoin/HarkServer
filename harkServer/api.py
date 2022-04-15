from flask import Flask, request
import json

import FusedDownloader
from db import getArticlesLastDayWithArticles
from db import jArticles
from fongUtils.fongLogger.CoreLogger import Log
Log = Log("Hark.Server.API", log_name="Hark.Server")

app = Flask(__name__)


@app.route('/articles', methods=['GET'])
def articles():
    Log.i("/articles called.", d=f"REQUEST={request}")
    arts = getArticlesLastDayWithArticles()
    Log.i(f"/articles: Returning {len(arts)} articles.")
    return json.dumps(arts, default=str)

@app.route('/articles/search/<searchTerm>', methods=['GET'])
def search_articles(searchTerm):
    Log.i("/articles/search called.", d=f"REQUEST={request}")
    results = jArticles.SEARCH_ARTICLES(searchTerm)
    Log.i(f"/articles: Returning {len(results)} articles.")
    return json.dumps(results, default=str)

@app.route('/articles/download/', methods=['GET'])
def download_article():
    Log.i("/articles/download called.", d=f"REQUEST={request}")
    args = request.args
    url = args.get("url")
    print(url)
    result = FusedDownloader.download(url)
    Log.i(f"/articles/download: Returning article.")
    return json.dumps([result], default=str)


if __name__ == '__main__':
    port = 3671
    debug = True
    host = "0.0.0.0"
    Log.i(f"Starting API. Host={host}, Port={port}, Debug={debug}, LOG_LEVEL={Log.log_level}")
    app.run(host=host, port=port, debug=debug)

