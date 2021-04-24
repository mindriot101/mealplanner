import pytest


@pytest.mark.skip
def test_single_recipe(client):
    r = client.post(
        "/recipes",
        json={
            "name": "cheese on toast",
        },
    )

    assert r.status_code == 201
    assert r.json["name"] == "cheese on toast"
