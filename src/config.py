import logging

from src.enums import GraphicMode
from src.utils import di

# App
DEBUG = True
APP = 'Simple-XSS'
VERSION = '0.3'

# Hook
HOOK_FILE = 'hook.py'
HOOK_CLASS = 'Hook'

# Payload
PAYLOAD_FILE = 'payload.py'
PAYLOAD_CLASS = 'Payload'

# Plugin
PLUGIN_FILE = 'plugin.py'
PLUGIN_CLASS = 'Plugin'

# Logging
LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOGGING_LEVEL = logging.DEBUG

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.CLI

if not DEBUG:
    import typeguard

    typeguard.typechecked = lambda a: a



