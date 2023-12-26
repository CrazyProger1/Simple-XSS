from src.enums import GraphicMode

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.CLI

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

if not DEBUG:
    import typeguard

    typeguard.typechecked = lambda a: a
