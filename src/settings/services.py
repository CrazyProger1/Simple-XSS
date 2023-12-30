from pydantic import BaseModel

from src.utils import di, settings as setutil
from src.arguments.dependencies import current_arguments
from src.arguments.schemas import DefaultArgumentsSchema
from .dependencies import (
    settings_schema,
    current_settings
)
from .events import (
    settings_loaded,
    settings_saved
)
from .config import DEFAULT_SETTINGS_FILE


@di.injector.inject
def load_settings(
        schema: type[BaseModel] = settings_schema,
        arguments: DefaultArgumentsSchema = current_arguments):
    try:
        settings = setutil.load(schema=schema, file=arguments.settings_file)
    except (FileNotFoundError, setutil.exceptions.FormatError, ValueError):
        settings = schema()
        save_settings(settings=settings)

    di.injector.bind(current_settings, settings)
    settings_loaded()
    return settings


@di.injector.inject
def save_settings(
        settings: BaseModel = current_settings,
        arguments: DefaultArgumentsSchema = current_arguments):
    try:
        setutil.save(instance=settings, file=arguments.settings_file)
    except ValueError:
        setutil.save(instance=settings, file=DEFAULT_SETTINGS_FILE)
    settings_saved()
