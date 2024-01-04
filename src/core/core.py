import sys

from .events import (
    application_initialized,
    application_launched,
    application_terminated,
    async_mode_entered,
    arguments_parsed,
    settings_loaded,
    plugins_loaded
)

from .logic import run_logic
from .dependencies import (
    configurate_base_dependencies
)
from .services import arguments, plugins, settings
from .ui import run_ui


def initialize():
    configurate_base_dependencies()

    plugins.load_plugins()
    plugins_loaded()

    arguments.parse_arguments(args=sys.argv[1:])
    arguments_parsed()

    settings.load_settings()
    settings_loaded()

    async_mode_entered.add_listener(run_logic)


def run():
    application_launched()

    # Init stage
    initialize()
    application_initialized()

    # UI launch stage
    run_ui()

    application_terminated()
