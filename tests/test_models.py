import pytest

from sqlalchemy.exc import IntegrityError

from poetrybot.database import store
from poetrybot.database.models import User, Poet


@pytest.fixture
def db():
    store.connect("sqlite://")
    return store


def test_users_empty(db):
    s = db.session()
    assert s.query(User).all() == []
    db.session.remove()


def test_users_creation_with_default_parameters(db):
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

def test_poets_empty(db):
    s = db.session()
    assert s.query(Poet).all() == []
    db.session.remove()

def test_poets_creation_no_parameters(db):
    """Test poet creation without parameters."""

    s = db.session()
    s.add(Poet())

    with pytest.raises(IntegrityError):
        s.commit()

    db.session.remove()

def test_poets_creation(db):
    """Test poet creation."""

    poet_name = "Eugenio Montale"

    s = db.session()
    s.add(Poet(name=poet_name))
    s.commit()

    poet = s.query(Poet).one()
    assert poet.id == 1
    assert poet.name == poet_name

    s.add(Poet(name=poet_name))
    with pytest.raises(IntegrityError):
        s.commit()
    db.session.rollback()

    s.add(Poet(name=poet_name.upper()))
    with pytest.raises(IntegrityError):
        s.commit()

    db.session.remove()
