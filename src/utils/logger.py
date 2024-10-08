import logging
import logging.config

format = "%(asctime)s - %(levelname)s - %(filename)s: %(message)s"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standar": {
            "format": f"{format}",
            "datefmt": "%Y-%m-%d %I:%M:%S %p"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standar",
            "class": "logging.StreamHandler"
        }
    },
    "root": {
        "handlers": ["default"],
        "level": "INFO",
        "propagate": True
    }
}
logging.config.dictConfig(LOGGING)