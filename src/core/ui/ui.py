from src.utils import di

from .base import BaseUI
from .dependencies import UIDependencyContainer
from .events import UIEventChannel


@di.inject
async def launch(ui: BaseUI = UIDependencyContainer.current_ui):
    await ui.run()


def initialize():
    UIDependencyContainer.configure()


async def run_ui():
    initialize()
    UIEventChannel.ui_initialized()

    await launch()
    UIEventChannel.ui_terminated()
