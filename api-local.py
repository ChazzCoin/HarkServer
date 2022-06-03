from flask import Flask
from harkAPI.routeArticles import routeArticles_blueprint
from harkAPI.routeGlewMeTv import routeGlewMeTv_blueprint

app = Flask(__name__)
app.register_blueprint(routeArticles_blueprint)
app.register_blueprint(routeGlewMeTv_blueprint)

@app.route("/help")
def help_api():
    return "I will help you sir."

if __name__ == '__main__':
    port = 3671
    debug = True
    host = "0.0.0.0"
    print(f"Starting API-Local. Host={host}, Port={port}, Debug={debug}")
    app.run(host=host, port=port, debug=debug)

