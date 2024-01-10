import sys

from src.core import (
    arguments,
    logging,
    plugins,
    settings,
    context,
    ui,
    logic
)

from src.core.events import (
    application_initialized,
    application_launched,
    application_terminated,
    async_mode_entered
)

from src.core.dependencies import configurate_base_dependencies
from src.core.context.events import context_changed


def initialize():
    logging.configurate_logging()

    configurate_base_dependencies()

    plugins.load_plugins()


    arguments.parse_arguments(args=sys.argv[1:])

    settings.load_settings()

    context.create_context()

    async_mode_entered.add_listener(logic.run_logic)
    context_changed.add_listener(context.save_context)


def run():
    application_launched()

    initialize()
    application_initialized()

    ui.run_ui()

    application_terminated()
