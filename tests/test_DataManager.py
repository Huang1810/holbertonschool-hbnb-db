import unittest
from unittest.mock import MagicMock
from persistence.DataManager import DataManager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()

    def tearDown(self):
        pass

    def test_save_and_get(self):
        mock_entity = MagicMock()
        mock_entity.id = 1
        self.data_manager.save(mock_entity)

        saved_entity = self.data_manager.get(1, type(mock_entity).__name__)
        self.assertEqual(saved_entity, mock_entity)

    def test_update(self):
        mock_entity = MagicMock()
        mock_entity.id = 1
        self.data_manager.save(mock_entity)

        mock_entity.some_attribute = "updated_value"
        self.data_manager.update(mock_entity)

        updated_entity = self.data_manager.get(1, type(mock_entity).__name__)
        self.assertEqual(updated_entity.some_attribute, "updated_value")

    def test_delete(self):
        mock_entity = MagicMock()
        mock_entity.id = 1
        self.data_manager.save(mock_entity)

        self.data_manager.delete(1, type(mock_entity).__name__)
        deleted_entity = self.data_manager.get(1, type(mock_entity).__name__)
        self.assertIsNone(deleted_entity)


if __name__ == '__main__':
    unittest.main()
