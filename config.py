import os

# hooks
HOOKS_DIR = r'.\hooks'
HOOK_MAIN_FILE = 'hook.html'
HOOK_PACKAGE_FILE = 'package.toml'
DEFAULT_HOOK = os.path.join(HOOKS_DIR, 'default')

# payloads
PAYLOADS_DIR = r'.\payloads'
PAYLOAD_MAIN_FILE = 'payload.js'
PAYLOAD_PACKAGE_FILE = 'package.toml'
PAYLOAD_INIT_FILE = 'init.py'
DEFAULT_PAYLOAD = os.path.join(PAYLOADS_DIR, 'hello_world')

# tunneling
DEFAULT_TUNNELING_APP = 'ngrok'
USE_TUNNELING_APP = True

# server
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444

# options
SETTINGS_FILE = 'settings.toml'

# app
APP = 'Simple-XSS'
VERSION = '0.2'

# logging
LOGGING_LEVEL = 0
LOGGING_VERBOSITY = False
LOG_FILE = f'{APP}.log'


DEVELOPMENT_MODE = False
