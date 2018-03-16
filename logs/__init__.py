import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "f": {
            "format": ("%(asctime)s [%(levelname)s] "
                       "%(processName)s:%(process)d "
                       "%(module)s:%(funcName)s() "
                       "%(filename)s:%(lineno)d "
                       "= %(message)s"),
            "datefmt": "%a, %d %b %Y %H:%M:%S %z"
        }
    },
    "handlers": {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO}
        },
    "root": {
        'handlers': ['h'],
        'level': logging.INFO,
        },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)
