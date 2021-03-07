import logging

from poetrybot.database import store
from poetrybot.config import Config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)

config = Config.from_environ()
log = logging.getLogger(__name__)


def main():
    log.debug("Starting poetrybot")

    store.connect(config.DATABASE_URL)


if __name__ == "__main__":
    main()
