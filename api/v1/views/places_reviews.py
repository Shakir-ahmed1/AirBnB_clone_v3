#!/usr/bin/python3
""" view definetion of the user module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """ gets all reviews of a place """
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    places = []
    for p in pl.reviews:
        places.append(p.to_dict())
    return jsonify(places)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """ gets a review using the given id"""
    result = storage.get(Review, review_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """ deletes the review which matches review id """
    result = storage.get(Review, review_id)
    if result is None:
        abort(404)
    result.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    info = request.get_json()
    if 'user_id' not in info:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in info:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    us = storage.get(User, info.get('user_id'))
    if us is None:
        abort(404)
    info['place_id'] = place_id
    rv = Review(**info)
    rv.save()
    storage.save()
    return make_response(jsonify(rv.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a review with the given information """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    a = storage.get(Review, review_id)
    if a is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(a, key, request.get_json().get(key))
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
