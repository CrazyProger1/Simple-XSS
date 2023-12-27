import os

import pathvalidate
from loguru import logger

from src.config import (
    DEFAULT_SETTINGS_FILE,
    LOGGING_VERBOSITY,
    LOG_FILE,
    LOGGING_LEVEL
)
from src.dependencies import (
    injector,
    current_settings,
    current_arguments
)
from src.settings import DefaultSettingsSchema
from src.arguments import DefaultArgumentsSchema
from src.utils import arguments
from src.utils import settings


class Configurator:
    def __init__(self):
        self._arguments: DefaultArgumentsSchema | None = None
        self._settings: DefaultSettingsSchema | None = None

    def _configure_logging(self):
        if not LOGGING_VERBOSITY:
            logger.remove()

        logger.add(
            LOG_FILE,
            level=LOGGING_LEVEL,
            rotation='100 KB',
            compression='zip'
        )
        logger.info('Logging configured')

    def _configure_dependencies(self):
        injector.bind(current_arguments, self._arguments)
        injector.bind(current_settings, self._settings)
        logger.info('Dependencies bound')

    def _load_args(self):
        argparser = arguments.SchemedArgumentParser(schema=DefaultArgumentsSchema)
        self._arguments = argparser.parse_typed_args()
        logger.info('Arguments loaded')

    def _load_settings(self):
        file = self._arguments.settings_file
        try:
            pathvalidate.validate_filepath(file)
        except pathvalidate.ValidationError:
            logger.warning(f'Settings file path {file} is not valid')
            file = DEFAULT_SETTINGS_FILE

        if os.path.isfile(file):
            try:
                self._settings = settings.load(DefaultSettingsSchema, file)
                logger.info('Settings loaded')
                return
            except settings.exceptions.FormatError:
                logger.warning('Settings file has wrong format')

        else:
            logger.warning(f'Settings file {file} not exists')

        self._settings = DefaultSettingsSchema()
        settings.save(self._settings, file)
        self._arguments.settings_file = file
        logger.info('New settings file created')

    def configure(self):
        self._configure_logging()

        self._load_args()
        self._load_settings()

        self._configure_dependencies()
