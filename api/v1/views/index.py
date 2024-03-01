#!/usr/bin/python3
"""
Index.py structure script
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'])
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