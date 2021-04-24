def test_status(client):
    r = client.get("/planner/")

    assert r.status_code == 200
