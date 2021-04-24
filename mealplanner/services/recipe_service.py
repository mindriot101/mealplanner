from ..models import Ingredient, Recipe, Membership
from ..db import db


class InvalidForm(Exception):
    pass


class RecipeService:
    def create_recipe_and_memberships(self, form):
        if not form["name"].strip():
            raise InvalidForm()
        recipe = Recipe(name=form["name"])
        db.session.add(recipe)
        db.session.commit()

        num_memberships = (len(form) - 1) // 2
        for i in range(num_memberships):
            ingredient_name = form[f"ingredient-name-{i}"]
            ingredient_count = int(form[f"ingredient-count-{i}"])
            ingredient = Ingredient.query.filter(
                Ingredient.name == ingredient_name
            ).first()
            membership = Membership(
                ingredient=ingredient, recipes=recipe, count=ingredient_count
            )
            db.session.add(membership)
            db.session.commit()
