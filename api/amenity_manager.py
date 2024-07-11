from flask import request, jsonify, abort, Blueprint
from model.amenity import Amenity
from persistence.DataManager import DataManager
from db import db

amenity_blueprint = Blueprint('amenity_manager', __name__)
data_manager = DataManager()


def validate_amenity_data(data):
    if not data or 'name' not in data:
        abort(400, description="Missing required fields: 'name'")


@amenity_blueprint.route('/amenities', methods=['POST'])
def create_amenity():
    validate_amenity_data(request.json)
    name = request.json['name']


    if Amenity.query.filter_by(name=name).first():
        abort(409, description="Amenity name already exists")


    new_amenity = Amenity(name=name)
    try:
        db.session.add(new_amenity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while creating the amenity: {str(e)}")

    return jsonify(new_amenity.to_dict()), 201


@amenity_blueprint.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@amenity_blueprint.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id, description="Amenity not found")
    return jsonify(amenity.to_dict()), 200


@amenity_blueprint.route('/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id, description="Amenity not found")
    validate_amenity_data(request.json)

    new_name = request.json.get('name')
    if new_name and new_name != amenity.name:
        if Amenity.query.filter(Amenity.name == new_name, Amenity.id != amenity_id).first():
            abort(409, description="Amenity name already exists")
        amenity.name = new_name

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while updating the amenity: {str(e)}")

    return jsonify(amenity.to_dict()), 200

@amenity_blueprint.route('/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id, description="Amenity not found")
    try:
        db.session.delete(amenity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while deleting the amenity: {str(e)}")
    
    return '', 204
