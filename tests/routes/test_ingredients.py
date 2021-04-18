from mealplanner.db import db


def test_create_ingredient(client):
    r = client.post("/ingredients", json={"name": "cheese"})

    assert r.status_code == 201
    assert r.json["name"] == "cheese"
    assert r.json["fat"] is None
    assert r.json["saturated_fat"] is None
    assert r.json["carbohydrate"] is None
    assert r.json["protein"] is None


def test_no_duplicates(client):
    r = client.post("/ingredients", json={"name": "cheese"})
    assert r.status_code == 201

    r = client.post("/ingredients", json={"name": "cheese"})
    assert r.status_code == 400
    assert r.json["message"] == "integrity error"
