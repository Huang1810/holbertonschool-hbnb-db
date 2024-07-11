from persistence.IPersistenceManager import IPersistenceManager
import json
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
        entity_type = type(entity).__name__
        if entity_type not in self.storage:
            self.storage[entity_type] = {}
        self.storage[entity_type][entity.id] = entity
        entity.save()

    def get(self, entity_id, entity_type):
        if entity_type in self.storage:
            return self.storage[entity_type].get(entity_id)
        return None

    def update(self, entity):
        entity_type = type(entity).__name__
        if entity_type in self.storage and entity.id in self.storage[entity_type]:
            self.storage[entity_type][entity.id] = entity
            entity.save()
        else:
            raise ValueError("Entity not found in storage")

    def delete(self, entity_id, entity_type):
        if entity_type in self.storage and entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]
        else:
            raise ValueError("Entity not found in storage")
