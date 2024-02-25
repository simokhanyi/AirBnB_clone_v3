#!/usr/bin/python3
# api/v1/views/index.py
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
