from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

from .models import Poem


def get_a_random_poem(session):
    """Return a random poem."""
    try:
        return session.query(Poem).order_by(func.random()).limit(1).one()
    except NoResultFound:
        return None
