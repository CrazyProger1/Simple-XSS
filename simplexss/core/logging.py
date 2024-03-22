import logging

from simplexss.core.config import (
    APP,
    DEBUG,
    LOGGING_LEVEL,
    LOGGING_FORMAT
)

logging.basicConfig(
    level=LOGGING_LEVEL,
    filename=f'{APP}.log',
    filemode='w',
    format=LOGGING_FORMAT
)
logger = logging.getLogger(APP)
