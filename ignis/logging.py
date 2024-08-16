import os
import sys
from loguru import logger

LOG_DIR = os.path.expanduser("~/.ignis")
LOG_FILE = f"{LOG_DIR}/ignis.log"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} [<level>{level}</level>] {message}"


def configure_logger(debug: bool) -> None:
    logger.remove()

    if debug:
        LEVEL = "DEBUG"
    else:
        LEVEL = "INFO"

    logger.add(sys.stderr, colorize=True, format=LOG_FORMAT, level=LEVEL)
    logger.add(LOG_FILE, format=LOG_FORMAT, level="DEBUG", rotation="1 day")

    logger.level("INFO", color="<green>")
