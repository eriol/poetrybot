import pytest

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem, is_user_in_allow_list
from poetrybot.database.models import Poet, Poem, User

# First verses of L'assiuolo by Giovanni Pascoli
# https://it.wikisource.org/wiki/Myricae/In_campagna/L%27assiuolo
verses1 = """Dov’era la luna? chè il cielo
notava in un'alba di perla,
ed ergersi il mandorlo e il melo
parevano a meglio vederla.
Venivano soffi di lampi
da un nero di nubi laggiù;
veniva una voce dai campi:
chiù...
"""

# Il lampo by Giovanni Pascoli
# https://it.wikisource.org/wiki/Myricae/Tristezze/Il_lampo
verses2 = """E cielo e terra si mostrò qual era:

la terra ansante, livida, in sussulto;
il cielo ingombro, tragico, disfatto:
bianca bianca nel tacito tumulto
una casa apparì sparì d’un tratto;
come un occhio, che, largo, esterrefatto,
s’aprì si chiuse, nella notte nera.
"""

poet_name = "Giovanni Pascoli"


@pytest.fixture
def db():
    store.connect("sqlite:///:memory:")
    return store


@pytest.fixture
def poems(db):

    with db.get_session() as s:

        poet = Poet(name=poet_name)
        s.add(poet)
        s.commit()

        s.add(Poem(verses=verses1, poet_id=poet.id))
        s.add(Poem(verses=verses2, poet_id=poet.id))
        s.commit()


@pytest.fixture
def users(db):

    with db.get_session() as s:
        s.add(User(id=123456, name="eriol"))
        s.commit()


def test_get_a_random_poem(db, poems):

    with db.get_session() as s:

        poem = get_a_random_poem(s)
        assert poem.verses in [verses1, verses2]
        assert poem.author.name == poet_name


def test_is_user_in_accept_list(db, users):
    with db.get_session() as s:

        assert is_user_in_allow_list(s, user_id=123456)
        assert not is_user_in_allow_list(s, user_id=654321)
