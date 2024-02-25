#!/usr/bin/python3
"""
app.py to run the Flask
"""

from flask import Flask
from os import getenv
from flask import Flask, jsonify
from api.v1 import app_views
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app_views.route('/status', methods=['GET'])
def get_status():
    """Get status"""
    return jsonify({"status": "OK"})


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


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


app.register_blueprint(app_views)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
