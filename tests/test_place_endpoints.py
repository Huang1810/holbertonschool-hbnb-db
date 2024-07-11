import unittest
import json
from api.place_manager import data_manager
from app import app
from model.place import Place
from model.city import City
from model.user import User
from model.amenity import Amenity


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = data_manager
        self.data_manager.storage = {}

        # Crear datos iniciales
        self.city = City(name='Test City', country_code='US')
        self.data_manager.save(self.city)
        self.user = User(email='test@example.com', password='password')
        self.data_manager.save(self.user)
        self.amenity = Amenity(name='Wi-Fi')
        self.data_manager.save(self.amenity)

    def test_create_place(self):
        response = self.app.post('/places', json={
            'name': 'Test Place',
            'description': 'A test place',
            'address': '123 Test St',
            'city_id': self.city.id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': self.user.id,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 100,
            'max_guests': 4,
            'amenity_ids': [self.amenity.id]
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Place', str(response.data))

    def test_get_places(self):
        place = Place(name='Test Place', description='A test place', address='123 Test St', city_id=self.city.id,
                      latitude=40.7128, longitude=-74.0060, host_id=self.user.id, number_of_rooms=3,
                      number_of_bathrooms=2, price_per_night=100, max_guests=4, amenity_ids=[self.amenity.id])
        self.data_manager.save(place)
        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Place', str(response.data))

    def test_get_place(self):
        place = Place(name='Test Place', description='A test place', address='123 Test St', city_id=self.city.id,
                      latitude=40.7128, longitude=-74.0060, host_id=self.user.id, number_of_rooms=3,
                      number_of_bathrooms=2, price_per_night=100, max_guests=4, amenity_ids=[self.amenity.id])
        self.data_manager.save(place)
        response = self.app.get(f'/places/{place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Place', str(response.data))

    def test_update_place(self):
        place = Place(name='Test Place', description='A test place', address='123 Test St', city_id=self.city.id,
                      latitude=40.7128, longitude=-74.0060, host_id=self.user.id, number_of_rooms=3,
                      number_of_bathrooms=2, price_per_night=100, max_guests=4, amenity_ids=[self.amenity.id])
        self.data_manager.save(place)
        response = self.app.put(f'/places/{place.id}', json={
            'name': 'Updated Place',
            'description': 'An updated test place',
            'address': '456 Updated St'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Place', str(response.data))

    def test_delete_place(self):
        place = Place(name='Test Place', description='A test place', address='123 Test St', city_id=self.city.id,
                      latitude=40.7128, longitude=-74.0060, host_id=self.user.id, number_of_rooms=3,
                      number_of_bathrooms=2, price_per_night=100, max_guests=4, amenity_ids=[self.amenity.id])
        self.data_manager.save(place)
        response = self.app.delete(f'/places/{place.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.data_manager.get(place.id, 'Place'))


if __name__ == "__main__":
    unittest.main()
