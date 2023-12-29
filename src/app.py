from src.di import (
    configurate_base_dependencies,
    configurate_launcher_dependency
)
from src.logging.services import configurate_logging
from src.arguments.services import parse_arguments
from src.settings.services import load_settings
from src.plugins.services import load_plugins
from src.view.launchers import BaseLauncher
from src.view.dependencies import current_launcher
from src.utils import di
from src.events import application_initialized, application_terminated


def initialize():
    configurate_logging()
    configurate_base_dependencies()
    load_plugins()
    parse_arguments()
    configurate_launcher_dependency()
    load_settings()


@di.injector.inject
def launch(launcher: BaseLauncher = current_launcher):
    launcher.launch()


def run():
    initialize()
    application_initialized()
    launch()
    application_terminated()
