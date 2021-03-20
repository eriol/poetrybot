"""Tests for the poems blueprint."""

import pytest

# Il lampo by Giovanni Pascoli (CC BY-NC-SA 4.0)
# https://www.liberliber.it/online/autori/autori-p/giovanni-pascoli/myricae/
verses = """E cielo e terra si mostrò qual era:

la terra ansante, livida, in sussulto;
il cielo ingombro, tragico, disfatto:
bianca bianca nel tacito tumulto
una casa apparì sparì d’un tratto;
come un occhio, che, largo, esterrefatto,
s'aprì si chiuse, nella notte nera.
"""


@pytest.fixture
def poet(client):
    """Ensure a poet is present in the system."""
    poet = {"name": "Giovanni Pascoli"}
    # We use the API itself to create a poet to not have to import database stuff here.
    r = client.post("/poets", json=poet)
    return r.get_json()


def test_empty(client):
    """Test get all the poets when the database is empty."""
    r = client.get("/poems")
    assert r.status == "200 OK"
    assert r.get_json() == []


def test_preate_poem(client, poet):
    """Test poem creation."""

    r = client.post(
        "/poems", json={"title": "", "verses": verses, "poet_id": poet["id"]}
    )
    assert r.status == "201 CREATED"
    assert r.get_json() == {"id": 1, "poet_id": 1, "title": "", "verses": verses}

    r = client.post("/poems", json={"verses": verses, "poet_id": poet["id"]})
    assert r.status == "201 CREATED"
    assert r.get_json() == {"id": 2, "poet_id": 1, "title": None, "verses": verses}


def test_get_poem(client, poet):
    """Test get poem details."""

    r = client.get("/poems/1")
    assert r.status == "404 NOT FOUND"
    assert r.get_json() == {"error": "Not Found"}

    r = client.post(
        "/poems", json={"title": "", "verses": verses, "poet_id": poet["id"]}
    )
    assert r.status == "201 CREATED"

    r = client.get("/poems/1")
    assert r.status == "200 OK"
    assert r.get_json() == {"id": 1, "poet_id": 1, "title": "", "verses": verses}


def test_edit_poem(client, poet):
    """Test edit a poem."""

    r = client.post(
        "/poems", json={"title": "", "verses": verses, "poet_id": poet["id"]}
    )
    assert r.status == "201 CREATED"

    poem = {"verses": "E cielo e terra...", "poet_id": poet["id"]}
    r = client.put("/poems/1", json=poem)
    assert r.status == "200 OK"
    poem.update({"id": 1, "title": ""})
    assert r.get_json() == poem
