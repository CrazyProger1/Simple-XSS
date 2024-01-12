from src.utils import di
from .controller import BaseController, Controller


class LogicDependenciesContainer(di.DeclarativeContainer):
    current_controller: BaseController

    @classmethod
    def configure(cls):
        di.bind(LogicDependenciesContainer.current_controller, Controller())
