# data_manager.py
from persistence.IPersistenceManager import IPersistenceManager
import json
import os
from db import db


class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {}
        self.load_countries()

    def load_countries(self):
        try:
            with open('countries.json', 'r') as f:
                countries = json.load(f)
            self.storage['Country'] = {
                country['code']: country for country in countries}
        except FileNotFoundError:
            self.storage['Country'] = {}

    def save(self, entity):
        try:
            if os.getenv('USE_DATABASE') == 'True':
                db.session.add(entity)
                db.session.commit()
            else:
                entity_type = type(entity).__name__
                if entity_type not in self.storage:
                    self.storage[entity_type] = {}
                self.storage[entity_type][entity.id] = entity
                self._save_to_file(entity)
        except Exception as e:
            print(f"Error saving entity: {e}")

    def get(self, entity_id, entity_type):
        try:
            if os.getenv('USE_DATABASE') == 'True':
                return db.session.query(entity_type).get(entity_id)
            else:
                if entity_type in self.storage:
                    return self.storage[entity_type].get(entity_id)
                return None
        except Exception as e:
            print(f"Error getting entity: {e}")

    def update(self, entity):
        try:
            if os.getenv('USE_DATABASE') == 'True':
                db.session.merge(entity)
                db.session.commit()
            else:
                entity_type = type(entity).__name__
                if entity_type in self.storage and entity.id in self.storage[entity_type]:
                    self.storage[entity_type][entity.id] = entity
                    self._save_to_file(entity)
                else:
                    raise ValueError("Entity not found in storage")
        except Exception as e:
            print(f"Error updating entity: {e}")

    def delete(self, entity_id, entity_type):
        try:
            if os.getenv('USE_DATABASE') == 'True':
                entity = db.session.query(entity_type).get(entity_id)
                if entity:
                    db.session.delete(entity)
                    db.session.commit()
                else:
                    raise ValueError("Entity not found in database")
            else:
                if entity_type in self.storage and entity_id in self.storage[entity_type]:
                    del self.storage[entity_type][entity_id]
                    self._save_to_file(None, entity_type)
                else:
                    raise ValueError("Entity not found in storage")
        except Exception as e:
            print(f"Error deleting entity: {e}")
