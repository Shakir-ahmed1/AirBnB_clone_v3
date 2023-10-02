#!/usr/bin/python3
""" view definetion of the city module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from uuid import uuid4


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id):
    """ gets list of cities in state """
    result = storage.get(State, state_id)
    if result is not None:
        cities = []
        for ct in result.cities:
            cities.append(ct.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_cities(city_id):
    """ gets a city using the given city_id """
    result = storage.get(City, city_id)
    if result is None:
        abort(404)
    else:
        return jsonify(result.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ deletes a city using the given city_id """
    result = storage.get(City, city_id)
    if result is None:
        abort(404)
    result.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ creates a new city """
    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    info = request.get_json()
    info['state_id'] = state_id
    ct = City(**info)
    ct.save()
    storage.save()
    return make_response(jsonify(ct.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update a city using the provided info """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, request.get_json().get(key))
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
