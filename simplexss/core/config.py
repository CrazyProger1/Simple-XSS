import os

from dotenv import load_dotenv

load_dotenv()

# Logging settings
LOGGING_CONFIG_FILE = os.getenv("LOGGING_CONFIG_FILE", "logging.ini")
