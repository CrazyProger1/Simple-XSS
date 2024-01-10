from src.utils import di

from .dependencies import configurate_ui_dependencies, current_ui_dependency
from .events import ui_initialized, ui_terminated
from .base import BaseUI


@di.injector.inject
def launch(ui: BaseUI = current_ui_dependency):
    ui.run()


def initialize():
    configurate_ui_dependencies()


def run_ui():
    # UI init stage
    initialize()
    ui_initialized()

    # UI launch stage
    launch()
    ui_terminated()
