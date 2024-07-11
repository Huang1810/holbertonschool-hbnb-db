from flask import Blueprint, request, jsonify, abort
from persistence.DataManager import DataManager
from model.city import City
from model.country import Country
from db import db

country_city_manager_blueprint = Blueprint('country_city_manager', __name__)
data_manager = DataManager()

def validate_city_data(data):
    if not data or 'name' not in data or 'country_code' not in data:
        abort(400, description="Missing required fields: 'name' and/or 'country_code'")

@country_city_manager_blueprint.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.to_dict() for country in countries]), 200

@country_city_manager_blueprint.route('/countries/<string:country_code>', methods=['GET'])
def get_country(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        abort(404, description="Country not found")
    return jsonify(country.to_dict()), 200

@country_city_manager_blueprint.route('/countries/<string:country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        abort(404, description="Country not found")
    cities = City.query.filter_by(country_code=country_code).all()
    return jsonify([city.to_dict() for city in cities]), 200

@country_city_manager_blueprint.route('/cities', methods=['POST'])
def create_city():
    validate_city_data(request.json)
    name = request.json['name']
    country_code = request.json['country_code']

    if not Country.query.filter_by(code=country_code).first():
        abort(400, description="Invalid country code")

    if City.query.filter_by(name=name, country_code=country_code).first():
        abort(409, description="City name already exists in this country")

    city = City(name=name, country_code=country_code)
    try:
        db.session.add(city)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while creating the city: {str(e)}")

    return jsonify({"city_id": city.id, "city": city.to_dict()}), 201

@country_city_manager_blueprint.route('/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    return jsonify([city.to_dict() for city in cities]), 200

@country_city_manager_blueprint.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    city = City.query.get_or_404(city_id, description="City not found")
    return jsonify(city.to_dict()), 200

@country_city_manager_blueprint.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    city = City.query.get_or_404(city_id, description="City not found")
    validate_city_data(request.json)

    city.name = request.json.get('name', city.name)
    new_country_code = request.json.get('country_code', city.country_code)

    if new_country_code != city.country_code:
        if not Country.query.filter_by(code=new_country_code).first():
            abort(400, description="Invalid country code")
        if City.query.filter_by(name=city.name, country_code=new_country_code).first():
            abort(409, description="City name already exists in the new country")
        city.country_code = new_country_code

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while updating the city: {str(e)}")

    return jsonify(city.to_dict()), 200

@country_city_manager_blueprint.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = City.query.get_or_404(city_id, description="City not found")
    try:
        db.session.delete(city)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An error occurred while deleting the city: {str(e)}")
    
    return '', 204
