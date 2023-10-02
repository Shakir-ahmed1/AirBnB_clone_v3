#!/usr/bin/python3
""" view definetion of the amenity module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id=None):
    """ gets all amenities or one amenities """
    if amenity_id is None:
        result = []
        amenities = storage.all(Amenity)
        for am in amenities:
            result.append(amenities[am].to_dict())
        return jsonify(result)
    result = storage.get(Amenity, amenity_id)
    if result is not None:
        return jsonify(result.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ deletes the given amenity by id """
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)
    am.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ creates a new amenity """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    info = request.get_json()
    am = Amenity(**info)
    am.save()
    storage.save()
    return make_response(jsonify(am.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates amenity with the given id """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    a = storage.get(Amenity, amenity_id)
    if a is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(a, key, request.get_json().get(key))
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
