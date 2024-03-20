import logging

from simplexss.core.config import (
    APP,
    DEBUG,
    LOGGING_LEVEL,
    LOGGING_FORMAT
)

logger = logging.getLogger(APP)
logger.setLevel(LOGGING_LEVEL)

if DEBUG:
    try:
        import colorlog

        formatter = colorlog.ColoredFormatter(
            LOGGING_FORMAT,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
    except ImportError:
        pass
