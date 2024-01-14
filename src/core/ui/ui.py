from src.utils import di

from .types import BaseUI
from .dependencies import (
    UIDependencyContainer,
    configure_ui_dependencies
)
from .events import UIEventChannel


@di.inject
async def launch(ui: BaseUI = UIDependencyContainer.current_ui):
    await ui.run()


def initialize():
    configure_ui_dependencies()


async def run_ui():
    initialize()
    UIEventChannel.ui_initialized()

    await launch()
    UIEventChannel.ui_terminated()
