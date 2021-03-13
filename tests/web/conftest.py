import pytest

from poetrybot.config import Config
from poetrybot.web.application import create_app


@pytest.fixture()
def client():
    """Get a test client."""
    config = Config.from_environ(
        {"DATABASE_URL": "sqlite:///:memory:", "TELEGRAM_TOKEN": ""}
    )
    app = create_app(config)

    with app.test_client() as client:
        yield client
