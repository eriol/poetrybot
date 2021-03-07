import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


def main():
    log.debug("Starting poetrybot")


if __name__ == "__main__":
    main()
