from src.utils import di
from .controller import BaseController, Controller

current_controller = di.Dependency(BaseController)


def configurate_logic_dependencies():
    di.injector.bind(current_controller, Controller())
