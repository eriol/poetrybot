import pytest

from sqlalchemy.exc import ArgumentError

from poetrybot.database import store


def test_connect():

    with pytest.raises(ArgumentError):
        store.connect("")

    store.connect("sqlite:///:memory:")
