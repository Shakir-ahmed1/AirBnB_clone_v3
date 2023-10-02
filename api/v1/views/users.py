#!/usr/bin/python3
""" view definetion of the user module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id=None):
    """ gets all users or one amenities """
    if user_id is None:
        result = []
        users = storage.all(User)
        for us in users:
            result.append(users[us].to_dict())
        return jsonify(result)
    result = storage.get(User, user_id)
    if result is not None:
        return jsonify(result.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """ deletes the given user by id """
    am = storage.get(User, user_id)
    if am is None:
        abort(404)
    am.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """ creates a new user """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    info = request.get_json()
    am = User(**info)
    am.save()
    storage.save()
    return make_response(jsonify(am.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates user with the given id """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    a = storage.get(User, user_id)
    if a is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(a, key, request.get_json().get(key))
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
