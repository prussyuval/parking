import os
import logging
import logging.config
from logging import Logger, RootLogger
from typing import Union

from utils.settings import LOG_LEVEL

LOGGER = Union[Logger, RootLogger]
LOGGING_CONFIG = {
    'disable_existing_loggers': False,
    'formatters': {
        'silence': {'format': '[%(levelname)s] %(message)s'},
        'simple': {'format': '[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s] - %(message)s'},
        'verbose': {'format': '[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s] [%(process)d | %(thread)d] - %(message)s'}},
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'root': {
            'handlers': ['stdout'],
            'level': LOG_LEVEL
        }
    },
    'version': 1
}


def setup_logging(logger_name: str = 'root') -> LOGGER:
    log = logging.getLogger(logger_name)
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
    except ValueError:
        # create file and try again
        handlers = LOGGING_CONFIG['loggers'][logger_name]['handlers']
        for handler in handlers:
            logging_path = LOGGING_CONFIG['handlers'][handler].get('filename')
            if logging_path:
                os.makedirs(os.path.dirname(logging_path), exist_ok=True)
        logging.config.dictConfig(LOGGING_CONFIG)
    return log


logger = setup_logging()