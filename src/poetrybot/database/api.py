from sqlalchemy.sql.expression import func

from .models import Poem


def get_a_random_poem(session):
    """Return a random poem."""
    return session.query(Poem).order_by(func.random()).limit(1).one()
