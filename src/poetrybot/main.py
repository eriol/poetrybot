import logging

from poetrybot.config import Config
from poetrybot.database import store
from poetrybot.telegram.bot import run

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)

config = Config.from_environ()
log = logging.getLogger(__name__)


def main():
    log.debug("Starting poetrybot")

    store.connect(config.DATABASE_URL)

    run(config)


if __name__ == "__main__":
    main()
