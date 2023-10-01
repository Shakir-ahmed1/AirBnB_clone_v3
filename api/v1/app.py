#!/usr/bin/python3
""" api controller flask module """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def remove_session(exception):
    """ remove the current sql alchemy session """
    storage.close()


if __name__ == "__main__":
    host = '0.0.0.0' if not getenv('HBNB_API_HOST') else getenv('HBNB_API_HOST')
    port = '5000' if not getenv('HBNB_API_PORT') else getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
    print(app.url_map)
