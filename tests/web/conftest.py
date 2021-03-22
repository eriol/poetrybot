import pytest

from poetrybot.config import Config
from poetrybot.web.application import create_app

TEST_AUTH_TOKEN = "a super secret token"


@pytest.fixture()
def client():
    """Get a test client."""
    config = Config.from_environ(
        {
            "AUTH_TOKEN": TEST_AUTH_TOKEN,
            "DATABASE_URL": "sqlite:///:memory:",
            "TELEGRAM_TOKEN": "",
        }
    )
    app = create_app(config)

    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = TEST_AUTH_TOKEN
        yield client
