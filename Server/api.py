from flask import Flask, request
# from DataProvider.MetaverseData import MetaData
import json

from Mongo.mArticles import mArticles
from rsLogger import Log
Log = Log("TiffanyBot.API", log_name="TiffanyBot.API")

app = Flask(__name__)
# meta_data = MetaData()
db = mArticles.constructor()

@app.route('/articles', methods=['GET'])
def articles():
    Log.i("/articles called.", d=f"REQUEST={request}")
    arts = db.Find.search_all("bitcoin", limit=500)
    Log.i(f"/articles: Returning {len(arts)} articles.", d=f"articles={arts}")
    return json.dumps(arts, default=str)

# @app.route('/glewmetv/data', methods=['GET'])
# def glewmetv():
#     Log.i("/glewmetv/data called.", d=f"REQUEST={request}")
#     from Utils import FILE
#     meta_ticker_info = meta_data.data_top_meta_tickers_info
#     meta_price_info = meta_data.data_top_meta_price_info
#     meta_events = meta_data.data_metaverse_events
#     glewmetv_data = FILE.load_dict_from_file("glewmetv", FILE.glewmetv_path)
#     final_return = {
#         "meta_ticker_info": meta_ticker_info,
#         "meta_price_info": meta_price_info,
#         "glewmetv": glewmetv_data,
#         "events": meta_events
#     }
#     Log.i(f"/glewmetv/data: Returning MetaReport Package data.", d=f"JSON={final_return}")
#     return json.dumps(final_return, default=str)


if __name__ == '__main__':
    port = 3671
    debug = True
    host = "0.0.0.0"
    Log.i(f"Starting API. Host={host}, Port={port}, Debug={debug}, LOG_LEVEL={Log.log_level}")
    app.run(host=host, port=port, debug=debug)

