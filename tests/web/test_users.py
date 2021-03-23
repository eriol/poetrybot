"""Tests for the users blueprint."""


def test_empty(client):
    """Test get all the users when the database is empty."""
    r = client.get("/users")
    assert r.status == "200 OK"
    assert r.get_json() == []


def test_create_user(client):
    """Test user creation."""
    r = client.post("/users", json={})
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {
        "error": "Bad Request",
        "message": {
            "id": ["Missing data for required field."],
            "name": ["Missing data for required field."],
        },
    }

    user = {"name": "eriol"}
    r = client.post("/users", json=user)
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {
        "error": "Bad Request",
        "message": {
            "id": ["Missing data for required field."],
        },
    }

    user = {"id": 1, "name": "eriol"}
    r = client.post("/users", json=user)
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {
        "error": "Bad Request",
        "message": {
            "id": ["id must be greater than 99999."],
        },
    }

    user = {"id": 123456, "name": "eriol"}
    r = client.post("/users", json=user)
    assert r.status == "201 CREATED"
    assert r.get_json() == user

    r = client.post("/users", json=user)
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {
        "error": "Bad Request",
        "message": "user with the specified id already exists",
    }

    r = client.get("/users")
    assert r.status == "200 OK"
    assert r.get_json() == [user]
