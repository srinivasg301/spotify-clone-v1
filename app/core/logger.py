import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(_formatter)

        file_handler = RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=3)
        file_handler.setFormatter(_formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logger
