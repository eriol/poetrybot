import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.debug("Starting poetrybot")
