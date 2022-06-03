from flask import Blueprint
import os
import json
from harkDataProvider import Provider
routeGlewMeTv_blueprint = Blueprint('routeGlewMeTv', __name__)

cwd = os.getcwd() + "/harkDataProvider"
meta_ticker_info = Provider.load_dict_from_file("meta_info", cwd)
meta_price_info = Provider.load_dict_from_file("top_meta_price_info", cwd + "/GlewMeTv")
meta_events = Provider.load_dict_from_file("events", cwd + "/GlewMeTv")[:10]
glewmetv_data = Provider.load_dict_from_file("glewmetv", cwd + "/GlewMeTv")

@routeGlewMeTv_blueprint.route('/glewmetv/data', methods=['GET'])
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