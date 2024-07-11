from model.country_city import City
from flask import Blueprint, request, jsonify, abort
from persistence.DataManager import DataManager
from model.city import City

country_city_manager_blueprint = Blueprint('country_city_manager', __name__)
data_manager = DataManager()



@country_city_manager_blueprint.route('/countries', methods=['GET'])
def get_countries():
    countries = list(data_manager.storage.get('Country', {}).values())
    return jsonify(countries), 200


country_city_manager_blueprint = Blueprint('country_city_manager', __name__)
data_manager = DataManager()



@country_city_manager_blueprint.route('/countries', methods=['GET'])
def get_countries():
    countries = list(data_manager.storage.get('Country', {}).values())
    return jsonify(countries), 200



@country_city_manager_blueprint.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = data_manager.get(country_code, 'Country')
    if not country:
        abort(404, description="Country not found")
    return jsonify(country), 200



@country_city_manager_blueprint.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    if not data_manager.get(country_code, 'Country'):
        abort(404, description="Country not found")
    cities = [city.to_dict() for city in data_manager.storage.get(
        'City', {}).values() if city.country_code == country_code]
    return jsonify(cities), 200



@country_city_manager_blueprint.route('/cities', methods=['POST'])
def create_city():
    if not request.json or 'name' not in request.json or 'country_code' not in request.json:
        abort(400, "Missing required fields")

    name = request.json['name']
    country_code = request.json['country_code']

    if not data_manager.get(country_code, 'Country'):
        abort(400, "Invalid country code")

    existing_cities = [city for city in data_manager.storage.get('City', {}).values()
                       if city.name == name and city.country_code == country_code]
    if existing_cities:
        abort(409, "City name already exists in this country")

    city = City(name=name, country_code=country_code)
    data_manager.save(city)

    return jsonify({"city_id": city.id, "city": city.to_dict()}), 201



@country_city_manager_blueprint.route('/cities', methods=['GET'])
def get_cities():
    cities = [city.to_dict()
              for city in data_manager.storage.get('City', {}).values()]
    return jsonify(cities), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    return jsonify(city.to_dict()), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")

    if not request.json:
        abort(400, description="Missing required fields")

    city.name = request.json.get('name', city.name)
    city.country_code = request.json.get('country_code', city.country_code)

    if not data_manager.get(city.country_code, 'Country'):
        abort(400, description="Invalid country code")

    data_manager.update(city)
    return jsonify(city.to_dict()), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")

    data_manager.delete(city_id, 'City')
    return '', 204



@country_city_manager_blueprint.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    countries = list(data_manager.storage.get('Country', {}).values())
    country = next(
        (country for country in countries if country['code'] == country_code), None)
    if not country:
        abort(404, description="Country not found")
    return jsonify(country), 200



@country_city_manager_blueprint.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    countries = list(data_manager.storage.get('Country', {}).values())
    if not any(country['code'] == country_code for country in countries):
        abort(404, description="Country not found")
    cities = [city.to_dict() for city in data_manager.storage.get(
        'City', {}).values() if city.country_code == country_code]
    return jsonify(cities), 200



@country_city_manager_blueprint.route('/cities', methods=['POST'])
def create_city():
    if not request.json or 'name' not in request.json or 'country_code' not in request.json:
        abort(400, "Missing required fields")

    name = request.json['name']
    country_code = request.json['country_code']

    countries = list(data_manager.storage.get('Country', {}).values())
    if not any(country['code'] == country_code for country in countries):
        abort(400, "Invalid country code")

    existing_cities = [city for city in data_manager.storage.get('City', {}).values()
                       if city.name == name and city.country_code == country_code]
    if existing_cities:
        abort(409, "City name already exists in this country")

    city = City(name=name, country_code=country_code)
    data_manager.save(city)

    return jsonify({"city_id": city.id, "city": city.to_dict()}), 201



@country_city_manager_blueprint.route('/cities', methods=['GET'])
def get_cities():
    cities = [city.to_dict()
              for city in data_manager.storage.get('City', {}).values()]
    return jsonify(cities), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    return jsonify(city.to_dict()), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")

    if not request.json:
        abort(400, description="Missing required fields")

    city.name = request.json.get('name', city.name)
    city.country_code = request.json.get('country_code', city.country_code)

    countries = list(data_manager.storage.get('Country', {}).values())
    if not any(country['code'] == city.country_code for country in countries):
        abort(400, description="Invalid country code")

    data_manager.update(city)
    return jsonify(city.to_dict()), 200



@country_city_manager_blueprint.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")

    data_manager.delete(city_id, 'City')
    return '', 204
