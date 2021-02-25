from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

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


store = Store()
