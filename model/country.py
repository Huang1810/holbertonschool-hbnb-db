from db import db
from model.BaseModel import BaseModel


class Country(BaseModel):
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), unique=True)
    cities = db.relationship('City', backref='country', lazy=True)

    def __init__(self, name, code, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def __str__(self):
        return f"[Country] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'name': self.name,
            'code': self.code
        }
