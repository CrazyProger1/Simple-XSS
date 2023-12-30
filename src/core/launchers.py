from abc import ABC, abstractmethod

from src.core.events import application_launched
from src.utils import di
from .controller.controllers import BaseController
from .controller.dependencies import current_controller
from .events import async_mode_entered
from .view.dependencies import current_ui
from .view.ui import BaseUI


class BaseLauncher(ABC):
    @abstractmethod
    def launch(self): ...


class Launcher(BaseLauncher):
    @di.injector.inject
    def _launch_ui(self, ui: BaseUI = current_ui):
        ui.launch()

    @di.injector.inject
    async def _launch_controller(self, controller: BaseController = current_controller):
        await controller.launch()

    def launch(self):
        application_launched()
        async_mode_entered.add_listener(self._launch_controller)
        self._launch_ui()
