import pytest

from poetrybot.database import store
from poetrybot.database.models import User


@pytest.fixture
def db():
    store.connect("sqlite://")
    return store


def test_users_empty(db):
    s = db.session()
    assert s.query(User).all() == []
    db.session.remove()


def test_users_creation_with_default_values(db):
    """Test creation of an user without parameters."""
    s = db.session()
    s.add(User())
    s.commit()

    assert db.session.query(User).all() != []
    u = s.query(User).one()
    assert u.id == 1
    assert u.is_staff is False

    db.session.remove()


def test_users_creation_staff(db):
    """Test creation of a staff user."""
    s = db.session()
    s.add(User(is_staff=True))
    s.commit()

    u = s.query(User).one()
    assert u.id == 1
    assert u.is_staff is True

    db.session.remove()
