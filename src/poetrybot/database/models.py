from sqlalchemy import Column, Integer, Boolean

from . import Base


class User(Base):
    """An user of poetrybot.

    Staff users can add/modify/delete poems.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    is_staff = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, is_staff={self.is_staff})"
