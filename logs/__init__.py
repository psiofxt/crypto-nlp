import logging
from logging.config import dictConfig
import sys

logging_config = dict(
    version=1,
    disable_existing_loggers=True,

    root={
        "level": "DEBUG",
        "handlers": ["console", "info_file_handler", "error_file_handler"]
    }

    loggers={
        """"root": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        },
        "sanic.error": {
            "level": "ERROR",
            "handlers": ["error_file_handler"],
            "propagate": False,
            "qualname": "sanic.error"
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": False,
            "qualname": "sanic.access"
        }"""
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "LEVEL": "DEBUG"
            "formatter": "generic",
            "stream": sys.stdout
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "../../temp/info.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "encoding": "utf8",
            "formatter": "generic"
        },
        "access_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "../../temp/info.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "encoding": "utf8",
            "formatter": "access"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "../../temp/error.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "encoding": "utf8",
            "formatter": "generic"
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                      "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
    }
)

#dictConfig(logging_config)
#logger = logging.getLogger(__name__)
