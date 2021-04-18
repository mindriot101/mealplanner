from mealplanner.db import db


def test_create_ingredient(client, mocker):
    uuidfn = mocker.MagicMock(return_value="uuid")
    uuid4 = mocker.patch("uuid.uuid4", uuidfn)

    r = client.post("/ingredients", json={"name": "cheese"})

    assert r.status_code == 201
    assert r.json["name"] == "cheese"
    assert r.json["fat"] is None
    assert r.json["saturated_fat"] is None
    assert r.json["carbohydrate"] is None
    assert r.json["protein"] is None
