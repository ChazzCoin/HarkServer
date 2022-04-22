import os

from flask import Flask, request
import json
import harkDB
from Downloader import FusedDownloader

app = Flask(__name__)

from harkFAIR.Core import FILE
cwd = os.getcwd() + "/harkDataProvider"
meta_ticker_info = FILE.load_dict_from_file("meta_info", cwd)
meta_price_info = FILE.load_dict_from_file("top_meta_price_info", cwd+"/GlewMeTv")
meta_events = FILE.load_dict_from_file("events", cwd+"/GlewMeTv")[:10]
glewmetv_data = FILE.load_dict_from_file("glewmetv", cwd+"/GlewMeTv")

@app.route('/articles', methods=['GET'])
def articles():
    print(f"/articles called. REQUEST={request}")
    arts = harkDB.getArticlesLastDayWithArticles()
    print(f"/articles: Returning articles.")
    return json.dumps(arts, default=str)

@app.route('/articles/search/<searchTerm>', methods=['GET'])
def search_articles(searchTerm):
    print("/articles/search called.", f"REQUEST={request}")
    results = harkDB.jArticles.SEARCH_ARTICLES(searchTerm)
    print(f"/articles/search: Returning articles.")
    return json.dumps(results, default=str)

@app.route('/articles/download/', methods=['GET'])
def download_article():
    print("/articles/download called. REQUEST={request}")
    args = request.args
    url = args.get("url")
    print(url)
    result = FusedDownloader.download(url)
    print(f"/articles/download: Returning article.")
    return json.dumps([result], default=str)

@app.route('/glewmetv/data', methods=['GET'])
def glewmetv():
    print("/glewmetv/data called. REQUEST={request}")
    final_return = {
        "meta_ticker_info": meta_ticker_info,
        "meta_price_info": meta_price_info,
        "glewmetv": glewmetv_data,
        "events": { "events": meta_events }
    }
    print(f"/glewmetv/data: Returning MetaReport Package data. JSON={final_return}")
    return json.dumps(final_return, default=str)


if __name__ == '__main__':
    port = 3671
    debug = True
    host = "0.0.0.0"
    print(f"Starting API-Local. Host={host}, Port={port}, Debug={debug}")
    app.run(host=host, port=port, debug=debug)

