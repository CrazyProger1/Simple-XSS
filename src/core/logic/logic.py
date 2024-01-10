from src.utils import di

from .dependencies import (
    configurate_logic_dependencies,
    current_controller_dependency
)
from .events import (
    logic_initialized,
    logic_terminated
)
from .controller import BaseController


def initialize():
    configurate_logic_dependencies()


@di.injector.inject
async def run_controller(controller: BaseController = current_controller_dependency):
    await controller.run()


async def run_logic():
    initialize()
    logic_initialized()

    await run_controller()
    logic_terminated()
