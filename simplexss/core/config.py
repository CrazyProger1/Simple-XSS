import logging
import os

from simplexss.core.enums import (
    GraphicMode,
)

RESOURCES_DIRECTORY = 'resources'

# App
DEBUG = True
APP = 'Simple-XSS'
VERSION = '0.3'

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.GUI.value
DEFAULT_THEME = 'dark'
DEFAULT_RESOLUTION = (1280, 760)
MIN_RESOLUTION = DEFAULT_RESOLUTION

# Plugins
PLUGINS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'plugins')
PLUGIN_FILE = 'plugin.py'

# Payloads
DEFAULT_PAYLOADS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'payloads')

# Hooks
DEFAULT_HOOKS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'hooks')

# Logging
LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOG_FILE_COMPRESSION = 'zip'
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(log_color)s%(levelname)s: %(name)s: %(message)s'

# Network
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444
DEFAULT_TRANSPORT = 'http'
DEFAULT_TUNNELING_SERVICE = 'serveo'
