import os

from dotenv import load_dotenv
from decouple import config

from src.core.logging import configure_logging

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
LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE", default="logging.ini")

# Settings config
SETTINGS_FILE = config("SETTINGS_FILE", default="settings.toml")

# Calling premain procedures
configure_logging(LOGGING_CONFIG_FILE)
