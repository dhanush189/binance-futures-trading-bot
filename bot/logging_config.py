import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = "futures_bot") -> logging.Logger:
    """Set up logger with rotating file handler and console handler."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
