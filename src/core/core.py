import sys

from src.utils import di
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
    configurate_base_dependencies,
    current_context
)
from .services import (
    arguments,
    plugins,
    settings,
    logging,
    context
)
from .ui import run_ui


def initialize():
    logging.configurate_logging()

    configurate_base_dependencies()

    plugins.load_plugins()
    plugins_loaded()

    arguments.parse_arguments(args=sys.argv[1:])
    arguments_parsed()

    settings.load_settings()
    settings_loaded()

    context.create_current_context()

    async_mode_entered.add_listener(run_logic)


@di.injector.inject
def destroy(appcontext: context.DefaultContext = current_context):
    settings.save_settings(settings=appcontext.settings)


def run():
    application_launched()

    # Init stage
    initialize()
    application_initialized()

    # UI launch stage
    run_ui()

    destroy()
    application_terminated()
