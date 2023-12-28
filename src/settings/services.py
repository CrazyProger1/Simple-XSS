from pydantic import BaseModel

from src.utils import di, settings as setutil
from src.arguments.dependencies import current_arguments
from src.arguments.schemas import DefaultArgumentsSchema
from .dependencies import (
    settings_schema,
    current_settings
)


@di.injector.inject
def load_settings(
        schema: type[BaseModel] = settings_schema,
        arguments: DefaultArgumentsSchema = current_arguments):
    settings = setutil.load(schema=schema, file=arguments.settings_file)
    di.injector.bind(current_settings, settings)
    return settings


@di.injector.inject
def save_settings(
        settings: BaseModel = current_settings,
        arguments: DefaultArgumentsSchema = current_arguments):
    setutil.save(instance=settings, file=arguments.settings_file)
