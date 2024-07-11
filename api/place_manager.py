from flask import request, jsonify, abort, Blueprint
from model.place import Place
from persistence.DataManager import DataManager
from db import db


place_manager_blueprint = Blueprint('place_manager', __name__)
data_manager = DataManager()



@place_manager_blueprint.route('/places', methods=['POST'])
def create_place():
    if not request.json:
        abort(400, description="Missing required fields")

    if Place.query.filter_by(name=request.json.get('name', '')).first():
        abort(409, description="Place already exists")

    place = Place(
        name=request.json.get('name', ''),
        description=request.json.get('description', ''),
        address=request.json.get('address', ''),
        city_id=request.json.get('city_id', ''),
        latitude=request.json.get('latitude', ''),
        longitude=request.json.get('longitude', ''),
        host_id=request.json.get('host_id', ''),
        number_of_rooms=request.json.get('number_of_rooms', ''),
        number_of_bathrooms=request.json.get('number_of_bathrooms', ''),
        price_per_night=request.json.get('price_per_night', ''),
        max_guests=request.json.get('max_guests', ''),
        amenity_ids=request.json.get('amenity_ids', '')
    )
    db.session.add(place)
    db.session.commit()

    return jsonify(place.to_dict()), 201



@place_manager_blueprint.route('/places', methods=['GET'])
def get_places():
    places = Place.query.all()
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list), 200



@place_manager_blueprint.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")
    return jsonify(place.to_dict()), 200



@place_manager_blueprint.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    if not request.json:
        abort(400, description="Missing required fields")

    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")

    if 'name' in request.json and Place.query.filter_by(name=request.json['name']).first():
        abort(409, description="Place with given name already exists")

    fields_to_update = ['name', 'description', 'address', 'city_id', 'latitude', 'longitude', 'host_id',
                        'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']
    for field in fields_to_update:
        if field in request.json:
            setattr(place, field, request.json[field])

    db.session.commit()
    return jsonify(place.to_dict()), 200



@place_manager_blueprint.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")

    db.session.delete(place)
    db.session.commit()
    return jsonify({"message": "Place deleted successfully"}), 200
