from src.enums import GraphicMode

# Settings
DEFAULT_SETTINGS_FILE = 'settings.toml'

# Graphic
DEFAULT_GRAPHIC_MODE = GraphicMode.CLI

# App
DEBUG = True
APP = 'Simple-XSS'
VERSION = '0.3'

if not DEBUG:
    import typeguard

    typeguard.typechecked = lambda a: a
