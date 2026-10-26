"""Logging (Day 2): record every API call, its inputs and timing so we can answer
'Where is my application going to break?'.

Logs go to the terminal AND to logs/app.log (rotating file).
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from app.config import settings


def setup_logging() -> logging.Logger:
    log = logging.getLogger("student_api")
    if log.handlers:  # already configured (uvicorn --reload can import twice)
        return log

    log.setLevel(logging.INFO)
    log.propagate = False
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    log.addHandler(console)

    try:
        folder = os.path.dirname(settings.log_file)
        if folder:
            os.makedirs(folder, exist_ok=True)
        file_handler = RotatingFileHandler(
            settings.log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(fmt)
        log.addHandler(file_handler)
    except OSError as exc:  # read-only disk on some hosts: keep console logging only
        log.warning("File logging disabled: %s", exc)

    return log


logger = setup_logging()
