from abc import ABC, abstractmethod

from src.core.ui.events import ui_process_activated, ui_process_deactivated
from src.core.dependencies import current_context
from src.utils import di


class BaseController(ABC):
    @abstractmethod
    async def run(self): ...


class Controller(BaseController):

    def __init__(self):
        ui_process_activated.add_listener(self._handle_process_activated)
        ui_process_deactivated.add_listener(self._handle_process_deactivated)

    @di.injector.inject
    async def _handle_process_activated(self, context=current_context):
        context.active = True

    @di.injector.inject
    async def _handle_process_deactivated(self, context=current_context):
        context.active = False

    async def run(self):
        print('APPLICATION LAUNCHED')
