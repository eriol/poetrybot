from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

from .models import Poem, User, Poet


def get_a_random_poem(session, author=None, argument=None):
    """Return a random poem.

    Filter by author and argument if specified.
    """
    try:
        query = session.query(Poem).join(Poem.author)

        if author is not None:
            query = query.options(contains_eager(Poem.author)).filter(
                Poet.name.like(f"%{author}%")
            )
        if argument is not None:
            query = query.filter(Poem.verses.like(f"%{argument}%"))

        return query.order_by(func.random()).limit(1).one()

    except NoResultFound:
        return None


def is_user_in_allow_list(session, user_id):
    """Return True if the user is inside the allow list."""
    return True if session.query(User).filter(User.id == user_id).count() else False
