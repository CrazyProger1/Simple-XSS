from src.utils import di

from .dependencies import (
    configurate_logic_dependencies,
    current_controller_dependency
)
from .events import (
    logic_initialized,
    logic_terminated
)


def initialize():
    configurate_logic_dependencies()


@di.injector.inject
async def run_controller(controller=current_controller_dependency):
    await controller.run()


async def run_logic():
    # Logic init stage
    initialize()
    logic_initialized()

    # Logic launch stage
    await run_controller()
    logic_terminated()
