from loguru import logger

from .config import (
    LOGGING_VERBOSITY,
    LOG_FILE,
    LOGGING_LEVEL
)


def configurate_logging():
    if not LOGGING_VERBOSITY:
        logger.remove()

    logger.add(
        LOG_FILE,
        level=LOGGING_LEVEL,
        rotation='100 KB',
        compression='zip'
    )
