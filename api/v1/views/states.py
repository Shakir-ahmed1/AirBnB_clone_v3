#!/usr/bin/python3
""" view definetion of the state module """
from api.v1.views import app_views
from flask import jsonify, abort, make_response
from models import storage
from models.state import State
from uuid import uuid4


@app_views.route('/states')
@app_views.route('/states/<state_id>')
def get_states(state_id=None, strict_slashes=False):
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


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_states(state_id):
    """ deletes the given state by id """
    sts = storage.get(State, state_id)
    if not sts:
        abort(404)
    sts.delete()
    storage.save()
    return make_response(jsonify({}), 200)
