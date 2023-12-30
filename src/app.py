from src.di import (
    configurate_base_dependencies
)
from src.events import (
    application_initialized,
    application_terminated
)
from src.utils import di
from src.logging.services import configurate_logging
from src.arguments.services import parse_arguments
from src.settings.services import load_settings
from src.plugins.services import load_plugins
from src.core.launchers import BaseLauncher
from src.core.dependencies import current_launcher


class App:
    def __init__(self):
        configurate_logging()
        configurate_base_dependencies()
        load_plugins()
        parse_arguments()
        load_settings()
        application_initialized()

    @di.injector.inject
    def _launch(self, launcher: BaseLauncher = current_launcher):
        launcher.launch()

    def run(self):
        self._launch()
        application_terminated()
