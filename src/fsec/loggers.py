""" Logger definitions """

import logging
import logging.config
import os
from collections import defaultdict


from version import __release__

try:
    from settings import LOGLEVEL
except ImportError:
    print("Could not find LOGLEVEL in settings.")
    LOGLEVEL = logging.DEBUG

try:
    from settings import LOGDIR
except ImportError:
    print("Could not find LOGDIR in settings.")
    LOGDIR = "./log"


if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)


def logging_config(level: int) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s()] %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "funcnames": {
                "format": "[%(name)s: %(lineno)s - %(funcName)s()] %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "layman": {"format": "%(message)s", "datefmt": "%Y-%m-%d %H:%M:%S"},
        },
        "handlers": {
            "console": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "layman",
            },
            "file_handler": {
                "level": level,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "funcnames",
                "filename": f"log/{__release__}.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 20,
            },
        },
        "root": {"level": level, "handlers": ["console", "file_handler"]},
    }


def standard_config(verbosity: int = -1):

    levels = defaultdict(
        lambda: LOGLEVEL,
        {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG},
    )

    logging.config.dictConfig(logging_config(levels[verbosity] or LOGLEVEL))
    logger = logging.getLogger()
    # logger.setLevel(levels[verbosity])
    logger.debug(
        f"Configured loggers (level: {logger.level}): {[x.name for x in logger.handlers]}"
    )


if __name__ == "__main__":

    standard_config()
    logger = logging.getLogger()
    logger.error("test-message")
