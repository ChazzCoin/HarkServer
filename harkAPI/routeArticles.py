from flask import Blueprint, request
import harkDB
from FusedDL import FusedDownloader
import json
routeArticles_blueprint = Blueprint('routeArticles', __name__)

@routeArticles_blueprint.route('/arts')
def index_articles():
    return "This is an example app"

@routeArticles_blueprint.route('/articles', methods=['GET'])
def articles():
    print(f"/articles called. REQUEST={request}")
    arts = harkDB.getArticlesLastDayWithArticles()
    print(f"/articles: Returning articles.")
    return json.dumps(arts, default=str)

@routeArticles_blueprint.route('/articles/count', methods=['GET'])
def article_count():
    print(f"/articles called. REQUEST={request}")
    arts_count = harkDB.collectionArticles.get_document_count()
    results = { "count": str(arts_count) }
    print(f"/articles: Returning articles.")
    return json.dumps(results, default=str)

@routeArticles_blueprint.route('/articles/search/<searchTerm>', methods=['GET'])
def search_articles(searchTerm):
    print("/articles/search called.", f"REQUEST={request}")
    results = harkDB.jArticles.SEARCH_ARTICLES(searchTerm)
    print(f"/articles/search: Returning articles.")
    return json.dumps(results, default=str)

@routeArticles_blueprint.route('/articles/download/', methods=['GET'])
def download_article():
    print("/articles/download called. REQUEST={request}")
    args = request.args
    url = args.get("url")
    print(url)
    result = FusedDownloader.download(url)
    print(f"/articles/download: Returning article.")
    return json.dumps([result], default=str)