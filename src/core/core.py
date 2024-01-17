from src.core import (
    arguments,
    logging,
    plugins,
    settings,
    data,
    ui,
    logic
)

from src.core.events import ApplicationEventChannel
from src.core.dependencies import configure_base_dependencies
from src.core.data.events import DataEventChannel


def initialize():
    logging.configurate_logging()

    configure_base_dependencies()

    plugins.load_plugins()

    arguments.parse_arguments()

    settings.load_settings()

    DataEventChannel.context_changed.add_listener(data.save_contexts)


async def run():
    ApplicationEventChannel.application_launched()

    initialize()
    ApplicationEventChannel.application_initialized()

    await logic.run_logic()
    await ui.run_ui()

    ApplicationEventChannel.application_terminated()
