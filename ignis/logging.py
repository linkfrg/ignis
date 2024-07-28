import logging
import os
import sys

LOG_DIR = os.path.expanduser("~/.ignis")
LOG_FILE = f"{LOG_DIR}/ignis.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

os.makedirs(LOG_DIR, exist_ok=True)

COLORS = {
    "DEBUG": "\033[36m",  # Cyan
    "INFO": "\033[32m",  # Green
    "WARNING": "\033[33m",  # Yellow
    "ERROR": "\033[31m",  # Red
    "CRITICAL": "\033[41m",  # Red background
}

RESET = "\033[0m"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, RESET)
        record.levelname = f"{log_color}{record.levelname}{RESET}"
        return super().format(record)


class FileFormatter(logging.Formatter):
    def format(self, record):
        for i in COLORS:
            if i in record.levelname:
                record.levelname = i

        return super().format(record)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("ignis")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE)

    if "--debug" in sys.argv:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    file_handler.setLevel(logging.DEBUG)

    console_formatter = ColorFormatter(LOG_FORMAT)
    file_formatter = FileFormatter(LOG_FORMAT)

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
