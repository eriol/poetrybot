import pytest

from poetrybot.config import Config
from poetrybot.web.application import create_app


@pytest.fixture
def client():
    config = Config.from_environ(
        {"DATABASE_URL": "sqlite:///:memory:", "TELEGRAM_TOKEN": ""}
    )
    app = create_app(config)

    with app.test_client() as client:
        yield client


def test_empty(client):
    """Test get all the poets when the database is empty."""
    r = client.get("/poets")
    assert r.status == "200 OK"
    assert r.get_json() == []


def test_create_poet(client):
    """Test poet creation."""
    r = client.post("/poets", json={})
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {"error": "Bad Request", "message": "name field is required"}

    poet = {"name": "Eugenio Montale"}
    r = client.post("/poets", json=poet)
    assert r.status == "201 CREATED"
    poet.update({"id": 1})
    assert r.get_json() == poet

    r = client.post("/poets", json=poet)
    assert r.status == "400 BAD REQUEST"
    assert r.get_json() == {
        "error": "Bad Request",
        "message": "this poet is already present",
    }

    r = client.get("/poets")
    assert r.status == "200 OK"
    assert r.get_json() == [poet]


def test_get_poet(client):
    """Test get poet details."""
    r = client.get("/poets/10")
    assert r.status == "404 NOT FOUND"
    assert r.get_json() == {"error": "Not Found"}

    poet = {"name": "Eugenio Montale"}
    r = client.post("/poets", json=poet)
    assert r.status == "201 CREATED"

    poet.update({"id": 1})
    r = client.get(f"/poets/{poet['id']}")
    assert r.status == "200 OK"
    assert r.get_json() == poet


def test_edit_poet(client):
    """Test edit a poet."""
    poet = {"name": "Eugenio M"}
    r = client.post("/poets", json=poet)
    assert r.status == "201 CREATED"
    poet = r.get_json()

    r = client.get(f"/poets/{poet['id']}")
    assert r.status == "200 OK"
    assert r.get_json() == poet

    poet = {"id": 1, "name": "Eugenio Montale"}
    r = client.put(f"/poets/{poet['id']}", json=poet)
    assert r.status == "200 OK"
    assert r.get_json() == poet


def test_delete_poet(client):
    """Test delete a poet."""
    poet = {"name": "Eugenio Montale"}
    r = client.post("/poets", json=poet)
    assert r.status == "201 CREATED"

    poet.update({"id": 1})
    r = client.get(f"/poets/{poet['id']}")
    assert r.status == "200 OK"

    r = client.delete(f"/poets/{poet['id']}")
    assert r.status == "204 NO CONTENT"

    r = client.get(f"/poets/{poet['id']}")
    assert r.status == "404 NOT FOUND"


def test_create_multiple_poets(client):
    """Test multiple poets creation."""
    poet1 = {"name": "Eugenio Montale"}
    poet2 = {"name": "Ugo Foscolo"}

    r = client.post("/poets", json=poet1)
    assert r.status == "201 CREATED"
    poet1 = r.get_json()
    r = client.post("/poets", json=poet2)
    assert r.status == "201 CREATED"
    poet2 = r.get_json()

    r = client.get("/poets")
    assert r.status == "200 OK"
    assert r.get_json() == [poet1, poet2]
