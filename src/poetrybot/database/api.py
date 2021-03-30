from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

from .models import Poem, User


def get_a_random_poem(session):
    """Return a random poem."""
    try:
        return session.query(Poem).order_by(func.random()).limit(1).one()
    except NoResultFound:
        return None


def is_user_in_accept_list(session, user_id):
    """Return True if the user is inside the accept list."""
    return True if session.query(User).filter(User.id == user_id).count() else False
