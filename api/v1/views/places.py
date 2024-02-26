#!/usr/bin/python3
"""
Module for handling RESTful API actions for Place objects
"""


from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places based on criteria in the request body."""
    # Parse JSON request body
    search_params = request.get_json()

    # Validate JSON format
    if not isinstance(search_params, dict):
        return jsonify({"error": "Not a JSON"}), 400

    # Extract search criteria
    states = search_params.get("states", [])
    cities = search_params.get("cities", [])
    amenities = search_params.get("amenities", [])

    # Retrieve all Place objects if no search criteria provided
    if not any([states, cities, amenities]):
        places = storage.all("Place").values()
    else:
        # Filter places based on search criteria
        places = set()
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    places.update(state.places)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)
        if amenities:
            amenity_objs = (
                [storage.get(Amenity, amenity_id) for amenity_id in amenities]
            )
            # Filter places that have all listed amenities
            for place in places.copy():
                if not all(amenity in place.amenities for amenity
                           in amenity_objs):
                    places.remove(place)

    # Serialize and return results
    return jsonify([place.to_dict() for place in places])
