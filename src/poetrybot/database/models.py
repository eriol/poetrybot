from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey

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


class Poet(Base):
    """A poet."""

    __tablename__ = "poets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150, collation="NOCASE"), nullable=False, unique=True)

    def __repr__(self):
        return f"Poet(id={self.id}, name={self.name})"

    def to_dict(self):
        """Return a dict representation of a poet."""
        return {"id": self.id, "name": self.name}


class Poem(Base):
    """A poem."""

    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255, collation="NOCASE"), nullable=True)
    verses = Column(Text(collation="NOCASE"), nullable=False)
    poet_id = Column(Integer, ForeignKey("poets.id"), nullable=False)
