#!/usr/bin/python3
""" view definetion of the state module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id=None):
    """ gets all states or one state """
    if state_id is None:
        result = []
        states = storage.all(State)
        for st in states:
            result.append(states[st].to_dict())
        return jsonify(result)
    result = storage.get(State, state_id)
    if result is not None:
        return jsonify(result.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states(state_id):
    """ deletes the given state by id """
    sts = storage.get(State, state_id)
    if sts is None:
        abort(404)
    sts.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ creates a new state """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    info = request.get_json()
    st = State(**info)
    st.save()
    storage.save()
    return make_response(jsonify(st.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates the given id """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    a = storage.get(State, state_id)
    if a is None:
        abort(404)
    for key in request.json:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(a, key, request.get_json().get(key))
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
