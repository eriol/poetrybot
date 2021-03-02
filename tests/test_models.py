import pytest

from sqlalchemy.exc import IntegrityError

from poetrybot.database import store
from poetrybot.database.models import User, Poet, Poem


@pytest.fixture
def db():
    store.connect("sqlite:///:memory:")
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


def test_poem_creation_no_parameters(db):
    """Test poem creation without parameters."""

    s = db.session()
    s.add(Poem())

    with pytest.raises(IntegrityError):
        s.commit()

    db.session.remove()


def test_poem_creation_no_poet(db):
    """Test poem creation without a poet."""

    s = db.session()

    # First verses of L'assiuolo by Giovanni Pascoli (CC BY-NC-SA 4.0)
    # https://www.liberliber.it/online/autori/autori-p/giovanni-pascoli/myricae/
    verses = """Dov’era la luna? ché il cielo
notava in un'alba di perla,
ed ergersi il mandorlo e il melo
parevano a meglio vederla.
Venivano soffi di lampi
da un nero di nubi laggiù;
veniva una voce dai campi:
chiù...
    """

    s.add(Poem(verses=verses))

    with pytest.raises(IntegrityError):
        s.commit()

    db.session.remove()


def test_poem_creation(db):
    """Test poem creation."""

    s = db.session()

    pascoli = Poet(name="Giovanni Pascoli")
    s.add(pascoli)
    s.commit()

    # First verses of L'assiuolo by Giovanni Pascoli (CC BY-NC-SA 4.0)
    # https://www.liberliber.it/online/autori/autori-p/giovanni-pascoli/myricae/
    verses = """Dov’era la luna? ché il cielo
notava in un'alba di perla,
ed ergersi il mandorlo e il melo
parevano a meglio vederla.
Venivano soffi di lampi
da un nero di nubi laggiù;
veniva una voce dai campi:
chiù...
    """

    s.add(Poem(verses=verses, poet_id=pascoli.id))
    s.commit()

    poem = s.query(Poem).one()
    assert poem.verses == verses

    db.session.remove()
