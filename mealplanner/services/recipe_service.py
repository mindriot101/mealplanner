from ..models import Ingredient, Recipe, Membership
from ..db import db


class InvalidForm(Exception):
    pass


class RecipeService:
    def create_recipe_and_memberships(self, form):
        if not form["name"].strip():
            raise InvalidForm("no name specified")

        recipe = self._create_recipe(form["name"])

        num_memberships = (len(form) - 1) // 2
        if num_memberships < 1:
            raise InvalidForm("no memberships found")

        for i in range(num_memberships):
            ingredient_name = form[f"ingredient-name-{i}"]
            ingredient_count_str = form[f"ingredient-count-{i}"]
            try:
                ingredient_count = int(ingredient_count_str)
            except ValueError:
                raise InvalidForm(f"count '{ingredient_count_str}' not an integer")
            self._create_membership(recipe, ingredient_name, ingredient_count)

    def get(self, id):
        return Recipe.query.get(id)

    def delete(self, id):
        recipe = self.get(id)
        db.session.delete(recipe)
        db.session.commit()

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
