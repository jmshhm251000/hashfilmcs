import logging.config
from pythonjsonlogger import jsonlogger


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs.log",
            "formatter": "json",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["stdout", "file"],
        "level": "DEBUG"
    }
}


logging.config.dictConfig(LOGGING)