from pydantic import BaseModel
from typeguard import typechecked

from src.utils import settings as setutil, di
from src.core.config import DEFAULT_SETTINGS_FILE
from src.core import arguments

from .dependencies import (
    SettingsDependencyContainer
)
from .events import (
    SettingsEventChannel
)


@typechecked
@di.inject
def load_settings(
        scheme: type[BaseModel] = SettingsDependencyContainer.settings_scheme,
        args: arguments.DefaultArgumentsScheme = arguments.ArgumentsDependencyContainer.current_arguments):
    file = args.settings_file
    try:
        settings = setutil.load(schema=scheme, file=file)
    except (FileNotFoundError, setutil.exceptions.FormatError, ValueError):
        settings = scheme()
        save_settings(settings=settings)

    di.bind(SettingsDependencyContainer.current_settings, settings)
    SettingsEventChannel.settings_loaded()
    return settings


@typechecked
@di.inject
def save_settings(
        settings=SettingsDependencyContainer.current_settings,
        args=arguments.ArgumentsDependencyContainer.current_arguments):
    file = args.settings_file
    try:
        setutil.save(instance=settings, file=file)
    except ValueError:
        setutil.save(instance=settings, file=DEFAULT_SETTINGS_FILE)
    SettingsEventChannel.settings_saved()
