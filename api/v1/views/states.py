#!/usr/bin/python3
"""
Module for handling RESTful API actions for State objects
"""


from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/stats', methods=['GET'], strict_slashes=False)
def get_state_stats():
    """Retrieves stats about State objects"""
    state_stats = {
        "__class__": "State",
        "created_at": "2017-04-14T00:00:02",
        "id": "8f165686-c98d-46d9-87d9-d6059ade2d99",
        "name": "Louisiana",
        "updated_at": "2017-04-14T00:00:02"
    }
    return jsonify(state_stats)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(app_views)
    app.run(host="0.0.0.0", port=5000)
