from src.utils import di
from .. import arguments
from src.core.arguments.dependencies import current_arguments_dependency
from .base import BaseUI, create_ui

current_ui_dependency = di.Dependency(BaseUI)


@di.injector.inject
def configurate_ui_dependencies(
        args: arguments.DefaultArgumentsScheme = current_arguments_dependency
):
    di.injector.bind(current_ui_dependency, create_ui(mode=args.graphic_mode))
