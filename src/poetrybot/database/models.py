"""Database models for poetrybot."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref


from . import Base


class User(Base):
    """An user of poetrybot."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Poet(Base):
    """A poet."""

    __tablename__ = "poets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150, collation="NOCASE"), nullable=False, unique=True)

    def __repr__(self):
        return f"Poet(id={self.id}, name={self.name})"


class Poem(Base):
    """A poem."""

    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255, collation="NOCASE"), nullable=True)
    verses = Column(Text(collation="NOCASE"), nullable=False)
    poet_id = Column(Integer, ForeignKey("poets.id"), nullable=False)

    author = relationship("Poet", backref=backref("poems"))

    def to_dict(self):
        """Return a dict representation of a poem."""
        return {
            "id": self.id,
            "title": self.title,
            "verses": self.verses,
            "poet_id": self.poet_id,
        }
