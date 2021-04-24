from ..models import Ingredient, Recipe, Membership
from ..db import db


class InvalidForm(Exception):
    pass


class RecipeService:
    def create_recipe_and_memberships(self, form):
        if not form["name"].strip():
            raise InvalidForm()

        recipe = self._create_recipe(form["name"])

        num_memberships = (len(form) - 1) // 2
        for i in range(num_memberships):
            ingredient_name = form[f"ingredient-name-{i}"]
            ingredient_count = int(form[f"ingredient-count-{i}"])
            self._create_membership(recipe, ingredient_name, ingredient_count)

    def _create_recipe(self, name):
        recipe = Recipe(name=name)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    def _create_membership(self, recipe, name, count):
        ingredient = Ingredient.query.filter(Ingredient.name == name).first()
        membership = Membership(ingredient=ingredient, recipes=recipe, count=count)
        db.session.add(membership)
        db.session.commit()
        return membership
