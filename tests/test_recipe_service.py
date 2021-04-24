import pytest

from mealplanner.services.recipe_service import RecipeService, InvalidForm
from mealplanner.models import Recipe, Membership, Ingredient
from mealplanner.db import db


def test_no_name():
    form = {"name": ""}
    service = RecipeService()

    with pytest.raises(InvalidForm):
        service.create_recipe_and_memberships(form)


def test_single_membership(app_context):
    ingredient = Ingredient(name="cheese")
    db.session.add(ingredient)
    db.session.commit()

    form = {"name": "recipe", "ingredient-name-0": "cheese", "ingredient-count-0": "5"}
    service = RecipeService()

    service.create_recipe_and_memberships(form)

    recipes = Recipe.query.all()
    assert len(recipes) == 1
    assert recipes[0].name == "recipe"

    memberships = Membership.query.all()
    assert len(memberships) == 1
    assert memberships[0].recipes == recipes[0]
    assert memberships[0].ingredient.name == "cheese"
    assert memberships[0].count == 5
