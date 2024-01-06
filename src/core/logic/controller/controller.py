from abc import ABC, abstractmethod

from src.core.ui.events import ui_process_activated, ui_process_deactivated
from src.core.context.dependencies import current_context
from src.core.dependencies import io_manager
from src.utils import di
from .enums import Messages


class BaseController(ABC):
    @abstractmethod
    async def run(self): ...


class Controller(BaseController):
    def __init__(self):
        ui_process_activated.add_listener(self._handle_process_activated)
        ui_process_deactivated.add_listener(self._handle_process_deactivated)
        self._io = di.injector.get_dependency(io_manager)

    @di.injector.inject
    async def _handle_process_activated(self, context=current_context, ):
        context.active = True

    @di.injector.inject
    async def _handle_process_deactivated(self, context=current_context):
        context.active = False

    async def run(self):
        await self._io.print(Messages.PROGRAM_LAUNCHED)
