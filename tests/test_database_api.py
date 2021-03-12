import pytest

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem
from poetrybot.database.models import Poet, Poem

# First verses of L'assiuolo by Giovanni Pascoli (CC BY-NC-SA 4.0)
# https://www.liberliber.it/online/autori/autori-p/giovanni-pascoli/myricae/
verses1 = """Dov’era la luna? ché il cielo
notava in un'alba di perla,
ed ergersi il mandorlo e il melo
parevano a meglio vederla.
Venivano soffi di lampi
da un nero di nubi laggiù;
veniva una voce dai campi:
chiù...
"""

# Il lampo by Giovanni Pascoli (CC BY-NC-SA 4.0)
# https://www.liberliber.it/online/autori/autori-p/giovanni-pascoli/myricae/
verses2 = """E cielo e terra si mostrò qual era:

la terra ansante, livida, in sussulto;
il cielo ingombro, tragico, disfatto:
bianca bianca nel tacito tumulto
una casa apparì sparì d’un tratto;
come un occhio, che, largo, esterrefatto,
s'aprì si chiuse, nella notte nera.
"""


@pytest.fixture
def db():
    store.connect("sqlite:///:memory:")
    return store


@pytest.fixture
def poems(db):

    with db.get_session() as s:

        pascoli = Poet(name="Giovanni Pascoli")
        s.add(pascoli)
        s.commit()

        s.add(Poem(verses=verses1, poet_id=pascoli.id))
        s.add(Poem(verses=verses2, poet_id=pascoli.id))
        s.commit()


def test_get_a_random_poem(db, poems):

    with db.get_session() as s:

        poem = get_a_random_poem(s)
        assert poem.verses in [verses1, verses2]
