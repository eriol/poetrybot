from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class Store:
    """A database access layer for poetrybot."""

    def __init__(self) -> None:
        self.connection_string = None
        self.engine = None

    def connect(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string)
        Base.metadata.create_all(self.engine)
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    @contextmanager
    def get_session(self):
        try:
            yield self.session()
        finally:
            self.session.remove()

    def rollback(self):
        self.session.rollback()


store = Store()
