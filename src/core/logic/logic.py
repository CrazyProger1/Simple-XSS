from src.utils import di

from .dependencies import configurate_logic_dependencies
from .events import (
    logic_initialized,
    logic_terminated
)


@di.injector.inject
def launch():
    pass


def initialize():
    configurate_logic_dependencies()


async def run_logic():
    # Logic init stage
    initialize()
    logic_initialized()

    # Logic launch stage
    launch()
    logic_terminated()
