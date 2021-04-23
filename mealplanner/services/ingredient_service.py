from ..models import Ingredient
from ..db import db


class IngredientService:
    def get(self, id):
        return Ingredient.query.get(id)

    def delete(self, id):
        ingredient = self.get(id)
        db.session.delete(ingredient)
        db.session.commit()

    def new_from_form(self, form):
        return Ingredient(
            name=form.name.data,
            fat=form.fat.data,
            saturated_fat=form.saturated_fat.data,
            carbohydrate=form.carbohydrate.data,
            protein=form.protein.data,
        )
