#!/usr/bin/python3
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

@app_views.route('/status')
def report_status():
    return jsonify({'status': 'ok'})

@app_views.route('/stats')
def view_stats():
    counts = {}
    for clss in classes:
        counts[clss] = storage.count(classes[clss])
    return jsonify(counts)
