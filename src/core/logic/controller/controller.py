from src.utils import di, io

from src.core.context import (
    DefaultContext,
    ContextDependenciesContainer
)
from src.core.ui import UIEventChannel

from src.core.io import IODependencyContainer

from .enums import Messages
from .base import BaseController


class Controller(BaseController):
    @di.inject
    def __init__(self, io_manager: io.AsyncIOManager = IODependencyContainer.io_manager):
        self._io = io_manager

    @di.inject
    async def _handle_process_activated(self, context: DefaultContext = ContextDependenciesContainer.current_context):
        context.process_active = True
        await self._io.info(Messages.LAUNCHING)
        abc = await self._io.input('abc')
        print(abc)

    @di.inject
    async def _handle_process_deactivated(self, context: DefaultContext = ContextDependenciesContainer.current_context):
        context.process_active = False

    async def run(self):
        UIEventChannel.ui_process_activated.add_listener(self._handle_process_activated)
        UIEventChannel.ui_process_deactivated.add_listener(self._handle_process_deactivated)
