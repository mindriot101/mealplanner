import pytest

from mealplanner.models import Recipe, Membership, Ingredient
from mealplanner.db import db


def test_deleting_ingredient_keeps_recipe(app_context):
    i1 = Ingredient(name="i1")
    i2 = Ingredient(name="i2")
    r = Recipe(name="r")
    m1 = Membership(ingredient=i1, recipes=r, count=1)
    m2 = Membership(ingredient=i2, recipes=r, count=2)

    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    db.session.delete(i2)
    db.session.commit()

    assert r.memberships == [m1]


def test_deleting_recipe_doesnt_delete_ingredient(app_context):
    i1 = Ingredient(name="i1")
    i2 = Ingredient(name="i2")
    r = Recipe(name="r")
    m1 = Membership(ingredient=i1, recipes=r, count=1)
    m2 = Membership(ingredient=i2, recipes=r, count=2)

    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    db.session.delete(r)
    db.session.commit()

    assert set(Ingredient.query.all()) == {i1, i2}
    assert list(Membership.query.all()) == []
