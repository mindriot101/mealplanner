import pytest

from mealplanner.models import Ingredient, Recipe
from mealplanner.db import db


@pytest.mark.skip
def test_add_ingredient(client):
    i = Ingredient(name="cheese")
    r = Recipe(name="cheese on toast")
    db.session.add_all([i, r])
    db.session.commit()

    res = client.patch(
        f"/recipes/{r.id}",
        json={
            "add": {
                "ingredient_id": str(i.id),
                "count": 5,
            },
        },
    )

    assert res.status_code == 200
    assert res.json["recipe"] == r.to_dict()
    # assert r.json["ingredient"] == i.to_dict()
    # assert r.json["count"] == 5
