import uuid

from sqlalchemy import UniqueConstraint

from .db import db
from .uuid_type import UUID


class Ingredient(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    fat = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    protein = db.Column(db.Float)
    membership = db.relationship(
        "Membership", cascade="all,delete-orphan", backref="ingredient"
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "fat": self.fat,
            "saturated_fat": self.saturated_fat,
            "carbohydrate": self.carbohydrate,
            "protein": self.protein,
        }


class Recipe(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    allocations = db.relationship(
        "Allocation",
        back_populates="recipe",
        cascade="all, delete",
        passive_deletes=True,
    )
    memberships = db.relationship(
        "Membership",
        cascade="all,delete-orphan",
        backref="recipes",
    )

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }


class Membership(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)
    ingredient_id = db.Column(UUID, db.ForeignKey("ingredient.id", ondelete="CASCADE"))
    recipe_id = db.Column(UUID, db.ForeignKey("recipe.id", ondelete="CASCADE"))
    count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "recipe": self.recipes.to_dict(),
            "ingredient": self.ingredient.to_dict(),
            "count": self.count,
        }


class Allocation(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)
    meal = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    recipe_id = db.Column(UUID, db.ForeignKey("recipe.id", ondelete="CASCADE"))
    recipe = db.relationship("Recipe", back_populates="allocations")

    __table_args__ = (UniqueConstraint("meal", "day", name="idx_allocation_meal_day"),)

    def __str__(self):
        return f"{self.recipe}"

    def to_dict(self):
        return {
            "id": str(self.id),
            "meal": self.meal,
            "day": self.day,
            "recipe": self.recipe.to_dict(),
        }
