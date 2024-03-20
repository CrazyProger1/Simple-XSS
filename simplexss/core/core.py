from simplexss.core.types import BaseCore
from simplexss.core.logging import logger
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)


class Core(BaseCore):
    def __init__(self, arguments: ArgumentsSchema, settings: SettingsSchema):
        self._arguments = arguments
        self._settings = settings
        logger.info('Core initialized')

    async def run(self):
        pass
