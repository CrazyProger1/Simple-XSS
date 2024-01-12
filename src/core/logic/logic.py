from src.utils import di

from .dependencies import (
    LogicDependenciesContainer
)
from .events import (
    LogicEventChannel
)


def initialize():
    LogicDependenciesContainer.configure()


@di.inject
async def run_controller(controller=LogicDependenciesContainer.current_controller):
    await controller.run()


async def run_logic():
    initialize()
    LogicEventChannel.logic_initialized()

    await run_controller()
    LogicEventChannel.logic_terminated()
