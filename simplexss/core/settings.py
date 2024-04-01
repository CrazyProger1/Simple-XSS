from pydantic import BaseModel

from simplexss.core.logging import logger
from simplexss.core.config import DEFAULT_SETTINGS_FILE
from simplexss.core.containers import CoreContainer
from simplexss.utils.di import inject
from simplexss.utils.settings import (
    BaseLoader,
)


@inject
def load_settings(
        schema: type[BaseModel] = CoreContainer.settings_schema,
        args=CoreContainer.arguments,
        loader: BaseLoader = CoreContainer.settings_loader):
    file = args.settings_file
    try:
        settings = loader.load(schema=schema, file=file)
    except Exception as e:
        settings = schema()
        save_settings(settings=settings)

    logger.info(f'Settings loaded: {settings}')
    return settings


@inject
def save_settings(
        settings=CoreContainer.settings,
        args=CoreContainer.arguments,
        loader: BaseLoader = CoreContainer.settings_loader):
    file = args.settings_file
    try:
        loader.save(data=settings, file=file)
    except ValueError:
        loader.save(data=settings, file=DEFAULT_SETTINGS_FILE)

    logger.info(f'Settings saved: {settings}')
