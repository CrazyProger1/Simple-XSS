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
    application_terminated
)

from src.core.dependencies import configurate_base_dependencies
from src.core.context.events import context_changed


def initialize():
    logging.configurate_logging()

    configurate_base_dependencies()

    plugins.load_plugins()

    arguments.parse_arguments()

    settings.load_settings()

    context.create_context()

    context_changed.add_listener(context.save_context)


async def run():
    application_launched()

    initialize()
    application_initialized()

    await logic.run_logic()
    await ui.run_ui()

    application_terminated()
