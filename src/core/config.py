import logging
import os

from .enums import GraphicMode

# App
DEBUG = True
APP = 'Simple-XSS'
VERSION = '0.3'

RESOURCES_DIRECTORY = 'resources'

if not DEBUG:
    import typeguard

    typeguard.typechecked = lambda a: a

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.GUI.value
DEFAULT_THEME = 'dark'
DEFAULT_RESOLUTION = (1280, 760)
MIN_RESOLUTION = DEFAULT_RESOLUTION

# Plugins
PLUGIN_FILE = 'plugin.py'
PLUGIN_CLASS_NAME = 'Plugin'
PLUGINS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'plugins')

# Payloads
DEFAULT_PAYLOADS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'payloads')
PAYLOAD_FILE = 'payload.py'
PAYLOAD_CLASS_NAME = 'Payload'

# Hooks
DEFAULT_HOOKS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'hooks')
HOOK_FILE = 'hook.py'
HOOK_CLASS_NAME = 'Hook'

# Logging
LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOG_FILE_COMPRESSION = 'zip'
LOGGING_LEVEL = logging.DEBUG
LOGGING_ROTATION = '10 MB'

# Network
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444
DEFAULT_TRANSPORT = 'http'
DEFAULT_TUNNELING_SERVICE = 'serveo'
