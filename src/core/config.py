import logging
import os

import flet as ft

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
DEFAULT_GRAPHIC_MODE = GraphicMode.GUI
DEFAULT_THEME = ft.ThemeMode.LIGHT
DEFAULT_RESOLUTION = (1280, 760)
MIN_RESOLUTION = DEFAULT_RESOLUTION

# Plugins
PLUGIN_FILE = 'plugin.py'
PLUGIN_CLASS_NAME = 'Plugin'
PLUGINS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'plugins')

# Payloads
PAYLOAD_FILE = 'payload.py'
PAYLOAD_CLASS_NAME = 'Payload'

# Hooks
HOOK_FILE = 'hook.py'
HOOK_CLASS_NAME = 'Hook'

# Logging
LOGGING_VERBOSITY = True
LOG_FILE = f'{APP}_{VERSION}.log'
LOGGING_LEVEL = logging.DEBUG
