#!/usr/bin/python3
""" view definetion of the user module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from uuid import uuid4


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """ gets all places of cities """
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    places = []
    for pl in ct.places:
        places.append(pl.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """ gets info of the give place_id """
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    return jsonify(pl.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ deletes a place with the given id """
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    pl.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    info = request.get_json()
    if 'name' not in info:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if 'user_id' not in info:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    us = storage.get(User, info.get('user_id'))
    if us is None:
        abort(404)
    info['city_id'] = city_id
    pl = Place(**info)
    pl.save()
    storage.save()
    return make_response(jsonify(pl.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place with the given information """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    a = storage.get(Place, place_id)
    if a is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(a, key, request.get_json().get(key))
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
