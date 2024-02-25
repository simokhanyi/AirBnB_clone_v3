#!/usr/bin/python3
"""
Module for handling RESTful API actions for State objects
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = State.all()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = State.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/stats', methods=['GET'], strict_slashes=False)
def get_state_stats():
    """Retrieves stats about State objects"""
    # Add your logic here to retrieve and return statistics about State objects
    return jsonify({'message': 'Stats about State objects'})


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
    state = State.get(state_id)
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
    state = State.get(state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200
