import pytest

from sqlalchemy.exc import IntegrityError

from poetrybot.database import store
from poetrybot.database.models import User, Poet, Poem


@pytest.fixture
def db():
    store.connect("sqlite:///:memory:")
    return store


def test_users_empty(db):
    with db.get_session() as s:
        assert s.query(User).all() == []


def test_users_creation_without_name(db):
    """Test creation of an user without name."""
    with db.get_session() as s:
        s.add(User())
        with pytest.raises(IntegrityError):
            s.commit()


def test_users_creation_with_name(db):
    """Test creation of a user with a name."""

    with db.get_session() as s:
        s.add(User(name="eriol"))
        s.commit()

        u = s.query(User).one()
        assert u.id == 1
        assert u.name == "eriol"


def test_poets_empty(db):
    with db.get_session() as s:
        assert s.query(Poet).all() == []


def test_poets_creation_no_parameters(db):
    """Test poet creation without parameters."""

    with db.get_session() as s:
        s.add(Poet())

        with pytest.raises(IntegrityError):
            s.commit()


def test_poets_creation(db):
    """Test poet creation."""
    poet_name = "Eugenio Montale"

    with db.get_session() as s:
        s.add(Poet(name=poet_name))
        s.commit()

        poet = s.query(Poet).one()
        assert poet.id == 1
        assert poet.name == poet_name

        s.add(Poet(name=poet_name))
        with pytest.raises(IntegrityError):
            s.commit()
        db.rollback()

        s.add(Poet(name=poet_name.upper()))
        with pytest.raises(IntegrityError):
            s.commit()


def test_poem_creation_no_parameters(db):
    """Test poem creation without parameters."""

    with db.get_session() as s:
        s = db.session()
        s.add(Poem())

        with pytest.raises(IntegrityError):
            s.commit()


def test_poem_creation_no_poet(db):
    """Test poem creation without a poet."""
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

    with db.get_session() as s:
        s.add(Poem(verses=verses))

        with pytest.raises(IntegrityError):
            s.commit()


def test_poem_creation(db):
    """Test poem creation."""
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

    with db.get_session() as s:

        pascoli = Poet(name="Giovanni Pascoli")
        s.add(pascoli)
        s.commit()

        s.add(Poem(verses=verses, poet_id=pascoli.id))
        s.commit()

        poem = s.query(Poem).one()
        assert poem.verses == verses
