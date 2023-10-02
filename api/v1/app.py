#!/usr/bin/python3
""" api controller for the flask module """
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv as genv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(exception):
    """ remove the current sql alchemy session """
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """ handles error for 404 """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = '0.0.0.0' if not genv('HBNB_API_HOST') else genv('HBNB_API_HOST')
    port = '5000' if not genv('HBNB_API_PORT') else genv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
