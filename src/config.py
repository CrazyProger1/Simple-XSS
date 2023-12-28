import logging

from src.enums import GraphicMode

# App
DEBUG = True
APP = 'Simple-XSS'
VERSION = '0.3'

# Logging
LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOGGING_LEVEL = logging.DEBUG

RESOURCES_DIRECTORY = 'resources'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.CLI

if not DEBUG:
    import typeguard

    typeguard.typechecked = lambda a: a
