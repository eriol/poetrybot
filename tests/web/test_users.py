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


def test_get_user(client):
    """Test get user details."""
    r = client.get("/users/123456")
    assert r.status == "404 NOT FOUND"
    assert r.get_json() == {"error": "Not Found"}

    user = {"id": 123456, "name": "eriol"}
    r = client.post("/users", json=user)
    assert r.status == "201 CREATED"

    r = client.get("/users/123456")
    assert r.status == "200 OK"
    assert r.get_json() == user


def test_edit_user(client):
    """Test edit an user."""
    user = {"id": 123456, "name": "e"}
    r = client.post("/users", json=user)
    assert r.status == "201 CREATED"

    user = {"name": "eriol"}
    r = client.put("/users/123456", json=user)
    assert r.status == "200 OK"
    user.update({"id": 123456})
    assert r.get_json() == user


def test_delete_user(client):
    """Test delete an user."""
    user = {"id": 123456, "name": "eriol"}

    r = client.delete(f"/users/{user['id']}")
    assert r.status == "404 NOT FOUND"

    r = client.post("/users", json=user)
    assert r.status == "201 CREATED"

    r = client.get(f"/users/{user['id']}")
    assert r.status == "200 OK"

    r = client.delete(f"/users/{user['id']}")
    assert r.status == "204 NO CONTENT"

    r = client.get(f"/users/{user['id']}")
    assert r.status == "404 NOT FOUND"
