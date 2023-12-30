import logging

from src.core.config import (
    APP,
    VERSION
)

LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOGGING_LEVEL = logging.DEBUG
