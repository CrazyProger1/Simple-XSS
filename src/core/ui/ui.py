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
async def launch(ui: BaseUI = current_ui_dependency):
    await ui.run()


def initialize():
    configurate_ui_dependencies()


async def run_ui():
    initialize()
    ui_initialized()

    await launch()
    ui_terminated()
