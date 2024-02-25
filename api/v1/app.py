#!/usr/bin/python3
"""app.py to run the Flask"""

from flask import Flask, jsonify, request
from os import getenv
from models import storage
from api.v1.views import app_views
from models.state import State
from datetime import datetime, timedelta

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route('/status', methods=['GET'])
def get_status():
    """Get status"""
    return jsonify({"status": "OK"})


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about the number of objects by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)


@app.route('/api/v1/states/', methods=['POST'])
def create_state():
    """Creates a new State object"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400

    data = request.json
    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
