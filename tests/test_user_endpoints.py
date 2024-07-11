import unittest
import json
from api.user_manager import data_manager
from app import app
from model.user import User


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = data_manager
        self.data_manager.storage = {}

    def test_create_user(self):
        response = self.app.post('/users', json={
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@example.com', str(response.data))

    def test_get_users(self):
        user = User(email='test@example.com', password='password123',
                    first_name='Test', last_name='User')
        self.data_manager.save(user)
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@example.com', str(response.data))

    def test_get_user(self):
        user = User(email='test@example.com', password='password123',
                    first_name='Test', last_name='User')
        self.data_manager.save(user)
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@example.com', str(response.data))

    def test_update_user(self):
        user = User(email='test@example.com', password='password123',
                    first_name='Test', last_name='User')
        self.data_manager.save(user)
        response = self.app.put(f'/users/{user.id}', json={
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated', str(response.data))

    def test_delete_user(self):
        user = User(email='test@example.com', password='password123',
                    first_name='Test', last_name='User')
        self.data_manager.save(user)
        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.data_manager.get(user.id, 'User'))


if __name__ == "__main__":
    unittest.main()
