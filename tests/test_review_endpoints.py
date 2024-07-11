import unittest
import json
from api.review_manager import data_manager
from app import app
from model.review import Review
from model.place import Place
from model.user import User


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = data_manager
        self.data_manager.storage = {}

        self.place = Place(name='Test Place', description='A test place', address='123 Test St', city_id='city123',
                           latitude=40.7128, longitude=-74.0060, host_id='host123', number_of_rooms=3,
                           number_of_bathrooms=2, price_per_night=100, max_guests=4, amenity_ids=[])
        self.data_manager.save(self.place)
        self.user = User(email='test@example.com', password='password')
        self.data_manager.save(self.user)
        self.host = User(email='host@example.com', password='password')
        self.data_manager.save(self.host)

    def test_create_review(self):
        response = self.app.post(f'/places/{self.place.id}/reviews', json={
            'user_id': self.user.id,
            'rating': 5,
            'comment': 'Great place!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Great place!', str(response.data))

    def test_get_user_reviews(self):
        review = Review(place_id=self.place.id,
                        user_id=self.user.id, rating=5, comment='Great place!')
        self.data_manager.save(review)
        response = self.app.get(f'/users/{self.user.id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Great place!', str(response.data))

    def test_get_place_reviews(self):
        review = Review(place_id=self.place.id,
                        user_id=self.user.id, rating=5, comment='Great place!')
        self.data_manager.save(review)
        response = self.app.get(f'/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Great place!', str(response.data))

    def test_get_review(self):
        review = Review(place_id=self.place.id,
                        user_id=self.user.id, rating=5, comment='Great place!')
        self.data_manager.save(review)
        response = self.app.get(f'/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Great place!', str(response.data))

    def test_update_review(self):
        review = Review(place_id=self.place.id,
                        user_id=self.user.id, rating=5, comment='Great place!')
        self.data_manager.save(review)
        response = self.app.put(f'/reviews/{review.id}', json={
            'rating': 4,
            'comment': 'Good place!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Good place!', str(response.data))

    def test_delete_review(self):
        review = Review(place_id=self.place.id,
                        user_id=self.user.id, rating=5, comment='Great place!')
        self.data_manager.save(review)
        response = self.app.delete(f'/reviews/{review.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.data_manager.get(review.id, 'Review'))


if __name__ == "__main__":
    unittest.main()
