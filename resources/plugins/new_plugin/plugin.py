from loguru import logger

from src.plugins import BasePlugin


class Plugin(BasePlugin):
    AUTHOR = 'crazyproger1'
    NAME = 'Test plugin'
    VERSION = '0.1'

    def __init__(self):
        logger.info('I AM SECOND PLUGIN')
