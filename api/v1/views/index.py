#!/usr/bin/python3
""" controlls the views of the blue print """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def report_status():
    """ returns the status of the route """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def view_stats():
    """ returns the stats of the route """
    counts = {}
    for clss in classes:
        counts[clss] = storage.count(classes[clss])
    return jsonify(counts)
