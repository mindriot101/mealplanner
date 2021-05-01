import pytest

from mealplanner.services.recipe_service import RecipeService, InvalidForm
from mealplanner.models import Recipe, Membership, Ingredient
from mealplanner.db import db


def test_no_name():
    form = {"name": ""}
    service = RecipeService()

    with pytest.raises(InvalidForm) as exc_info:
        service.create_recipe_and_memberships(form)

    assert str(exc_info.value) == "no name specified"


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
    assert memberships[0].recipe == recipes[0]
    assert memberships[0].ingredient.name == "cheese"
    assert memberships[0].count == 5


def test_two_memberships(app_context):
    i1 = Ingredient(name="cheese")
    i2 = Ingredient(name="toast")
    db.session.add_all([i1, i2])
    db.session.commit()

    form = {
        "name": "recipe",
        "ingredient-name-0": "cheese",
        "ingredient-count-0": "5",
        "ingredient-name-1": "toast",
        "ingredient-count-1": "12",
    }
    service = RecipeService()

    service.create_recipe_and_memberships(form)

    recipes = Recipe.query.all()
    assert len(recipes) == 1
    assert recipes[0].name == "recipe"

    memberships = Membership.query.all()
    assert len(memberships) == 2
    assert memberships[0].recipe == recipes[0]
    assert memberships[0].ingredient.name == "cheese"
    assert memberships[0].count == 5
    assert memberships[1].recipe == recipes[0]
    assert memberships[1].ingredient.name == "toast"
    assert memberships[1].count == 12


def test_no_memberships(app_context):
    form = {
        "name": "recipe",
    }
    service = RecipeService()

    with pytest.raises(InvalidForm) as exc_info:
        service.create_recipe_and_memberships(form)

    assert str(exc_info.value) == "no memberships found"


def test_number_validation(app_context):
    form = {
        "name": "recipe",
        "ingredient-name-0": "cheese",
        "ingredient-count-0": "not-an-integer",
    }
    service = RecipeService()

    with pytest.raises(InvalidForm) as exc_info:
        service.create_recipe_and_memberships(form)

    assert str(exc_info.value) == "count 'not-an-integer' not an integer"
