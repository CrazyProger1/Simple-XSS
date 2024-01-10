from src.utils import di

from .base import BaseUI
from .dependencies import (
    configurate_ui_dependencies,
    current_ui_dependency
)
from .events import (
    ui_initialized,
    ui_terminated
)


@di.injector.inject
def launch(ui: BaseUI = current_ui_dependency):
    ui.run()


def initialize():
    configurate_ui_dependencies()


def run_ui():
    initialize()
    ui_initialized()

    launch()
    ui_terminated()
