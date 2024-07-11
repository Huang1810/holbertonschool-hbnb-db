from model.BaseModel import BaseModel
from db import db
from model.country import Country


class City(BaseModel):
    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(
        db.String(2), db.ForeignKey('country.code'), nullable=True)
    place = db.relationship('Place', backref='city', lazy=True)

    def __init__(self, name, country_code, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __str__(self):
        return f"[City] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
