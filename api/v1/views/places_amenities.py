#!/usr/bin/python3
"""
Place-Amenity API endpoints
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieve list of all amenities of a place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity from a place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Link an amenity to a place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
