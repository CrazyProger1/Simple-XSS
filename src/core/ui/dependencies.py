from pydantic import BaseModel

from src.utils import di
from src.core.services import arguments, settings
from src.core.dependencies import current_arguments, current_settings
from .base import BaseUI, get_ui

current_ui = di.Dependency(BaseUI)
local_settings = di.Dependency(BaseModel)


@di.injector.inject
def configurate_ui_dependencies(
        args: arguments.DefaultArgumentsScheme = current_arguments,
        sets: settings.DefaultSettingsScheme = current_settings
):
    di.injector.bind(current_ui, get_ui(mode=args.graphic_mode)())
    di.injector.bind(local_settings, sets.model_copy())
