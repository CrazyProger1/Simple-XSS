from src.utils import di, io

from src.core.context.dependencies import current_context_dependency
from src.core.context import DefaultContext
from src.core.ui.events import (
    ui_process_activated,
    ui_process_deactivated
)
from src.core.io.dependencies import io_manager_dependency

from .enums import Messages
from .base import BaseController


class Controller(BaseController):
    @di.injector.inject
    def __init__(self, io_manager: io.AsyncIOManager = io_manager_dependency):
        self._io = io_manager

    @di.injector.inject
    async def _handle_process_activated(self, context: DefaultContext = current_context_dependency):
        context.process_active = True
        await self._io.info(Messages.LAUNCHING)
        abc = await self._io.input('abc')
        print(abc)

    @di.injector.inject
    async def _handle_process_deactivated(self, context: DefaultContext = current_context_dependency):
        context.process_active = False

    async def run(self):
        ui_process_activated.add_listener(self._handle_process_activated)
        ui_process_deactivated.add_listener(self._handle_process_deactivated)
