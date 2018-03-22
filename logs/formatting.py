
import logging
import logging.config

logging_config = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        "mine": {
            "level": "INFO",
            "handlers": ["info_file_handler"],
            "propagate": True
        }
    },
    handlers={
        "info_file_handler": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "level": "INFO",
            "filename": "/var/log/erebor/info.log",
            "encoding": "utf-8"
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        }
    }
)

logging.config.dictConfig(logging_config)
logger = logging.getLogger("mine")

logger.info("test from script in console")



# ----------------------------------------
import logging
logger = logging.getLogger("test")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("/var/log/erebor/infotest.log")
fh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.info("test from logging object and handler object")
