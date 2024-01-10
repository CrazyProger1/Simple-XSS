from src.utils import di
from .controller import BaseController, Controller

current_controller_dependency = di.Dependency(BaseController)


def configurate_logic_dependencies():
    di.injector.bind(current_controller_dependency, Controller())
