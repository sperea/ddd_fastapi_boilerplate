import logging
from logging.config import dictConfig
import os

LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOGS_DIR, "app.log"),
            "mode": "a",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

def init_logging():
    dictConfig(LOGGING_CONFIG)
