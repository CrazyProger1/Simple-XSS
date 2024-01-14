from src.utils import di

from .dependencies import (
    configure_logic_dependencies,
    LogicDependenciesContainer
)
from .events import (
    LogicEventChannel
)


@di.inject
async def activate_process(process=LogicDependenciesContainer.process):
    await process.activate()


@di.inject
async def deactivate_process(process=LogicDependenciesContainer.process):
    await process.deactivate()


def initialize():
    configure_logic_dependencies()


async def run_logic():
    from src.core.ui import UIEventChannel

    initialize()
    LogicEventChannel.logic_initialized()

    UIEventChannel.process_activated.add_listener(activate_process)
    UIEventChannel.process_deactivated.add_listener(deactivate_process)
