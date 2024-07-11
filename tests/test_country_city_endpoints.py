import unittest
import json
from api.country_city_manager import data_manager
from app import app
from model.city import City


class TestCountryCityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = data_manager
        self.data_manager.storage = {}
        self.data_manager.load_countries()

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        self.assertIn('United States', str(response.data))

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        self.assertIn('United States', str(response.data))

    def test_get_cities_by_country(self):
        city = City(name='New York', country_code='US')
        self.data_manager.save(city)
        response = self.app.get('/countries/US/cities')
        self.assertEqual(response.status_code, 200)
        self.assertIn('New York', str(response.data))

    def test_create_city(self):
        response = self.app.post('/cities', json={
            'name': 'Los Angeles',
            'country_code': 'US'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Los Angeles', str(response.data))

    def test_get_cities(self):
        city = City(name='Los Angeles', country_code='US')
        self.data_manager.save(city)
        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Los Angeles', str(response.data))

    def test_get_city(self):
        city = City(name='Los Angeles', country_code='US')
        self.data_manager.save(city)
        response = self.app.get(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Los Angeles', str(response.data))

    def test_update_city(self):
        city = City(name='Los Angeles', country_code='US')
        self.data_manager.save(city)
        response = self.app.put(f'/cities/{city.id}', json={
            'name': 'Updated City',
            'country_code': 'US'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated City', str(response.data))

    def test_delete_city(self):
        city = City(name='Los Angeles', country_code='US')
        self.data_manager.save(city)
        response = self.app.delete(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.data_manager.get(city.id, 'City'))


if __name__ == "__main__":
    unittest.main()
