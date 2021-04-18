import uuid

from .db import db
from .uuid_type import UUID


class Ingredient(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String, nullable=False)
    fat = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    protein = db.Column(db.Float)

    def to_dict(self):
        print(uuid.uuid4())
        return {
            "id": str(self.id),
            "name": self.name,
            "fat": self.fat,
            "saturated_fat": self.saturated_fat,
            "carbohydrate": self.carbohydrate,
            "protein": self.protein,
        }
