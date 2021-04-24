import pytest

from mealplanner.db import db
from mealplanner.models import Ingredient


@pytest.mark.skip
def test_create_ingredient(client):
    r = client.post("/api/ingredients", json={"name": "cheese"})

    assert r.status_code == 201
    assert r.json["name"] == "cheese"
    assert r.json["fat"] is None
    assert r.json["saturated_fat"] is None
    assert r.json["carbohydrate"] is None
    assert r.json["protein"] is None


@pytest.mark.skip
def test_no_duplicates(client):
    r = client.post("/ingredients", json={"name": "cheese"})
    assert r.status_code == 201

    r = client.post("/ingredients", json={"name": "cheese"})
    assert r.status_code == 400
    assert r.json["message"] == "integrity error"


def test_list_ingredients_no_entries(client):
    r = client.get("/api/ingredients")

    assert r.status_code == 200
    assert r.json == {"ingredients": []}


def test_list_ingredients(client):
    i = Ingredient(name="cheese")
    db.session.add(i)
    db.session.commit()

    r = client.get("/api/ingredients")

    assert r.status_code == 200
    assert [i["name"] for i in r.json["ingredients"]] == ["cheese"]
