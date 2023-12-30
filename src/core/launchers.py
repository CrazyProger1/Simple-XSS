from abc import ABC, abstractmethod

from src.utils import di
from src.arguments.dependencies import current_arguments
from src.arguments.schemas import DefaultArgumentsSchema
from src.events import application_launched
from .view.dependencies import current_ui
from .view.ui import get_ui, BaseUI


class BaseLauncher(ABC):

    @abstractmethod
    def launch(self): ...


class Launcher(BaseLauncher):
    @di.injector.inject
    def _configurate_dependencies(self, arguments: DefaultArgumentsSchema = current_arguments):
        di.injector.bind(current_ui, get_ui(arguments.graphic_mode))

    @di.injector.inject
    def _launch_ui(self, ui: BaseUI = current_ui):
        ui.launch()

    def launch(self):
        self._configurate_dependencies()
        application_launched()
        self._launch_ui()
