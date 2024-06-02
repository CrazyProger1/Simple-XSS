import os

from dotenv import load_dotenv

from simplexss.core.enums import GraphicMode
from simplexss.core.logging import configure_logging

# Loading .env file
load_dotenv()

# App config
APP = "Simple-XSS"
VERSION = "0.0.4"
DESCRIPTION = (
    "Simple-XSS is a multi-platform cross-site scripting (XSS) vulnerability exploitation tool for "
    "pentesting."
)

# Logging config
LOGGING_CONFIG_FILE = os.getenv("LOGGING_CONFIG_FILE", "logging.ini")

# Settings config
DEFAULT_SETTINGS_FILE = os.getenv("SETTINGS_FILE", "settings.toml")

# Graphics config
DEFAULT_GRAPHIC_MODE = os.getenv("GRAPHIC_MODE", GraphicMode.DESKTOP)

# i18n config
DEFAULT_LANGUAGE = os.getenv("LANGUAGE", "en")

# Calling premain procedures
configure_logging(LOGGING_CONFIG_FILE)
