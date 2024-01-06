from src.utils import di
from src.core.services import arguments
from src.core.dependencies import current_arguments
from .base import BaseUI, create_ui

current_ui = di.Dependency(BaseUI)


@di.injector.inject
def configurate_ui_dependencies(
        args: arguments.DefaultArgumentsScheme = current_arguments
):
    di.injector.bind(current_ui, create_ui(mode=args.graphic_mode))
