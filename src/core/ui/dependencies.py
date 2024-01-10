from src.utils import di
from src.core import arguments
from src.core.arguments.dependencies import current_arguments_dependency
from .factories import UIFactory
from .base import BaseUI

current_ui_dependency = di.Dependency(BaseUI)
ui_factory_dependency = di.Dependency(UIFactory, UIFactory)


@di.injector.inject
def configurate_ui_dependencies(
        args: arguments.DefaultArgumentsScheme = current_arguments_dependency,
        ui_factory: UIFactory = ui_factory_dependency
):
    di.injector.bind(current_ui_dependency, ui_factory.create_ui(mode=args.graphic_mode))
