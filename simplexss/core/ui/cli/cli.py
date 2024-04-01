from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from simplexss.core.containers import CoreContainer
from simplexss.core.logging import logger
from simplexss.utils.di import inject
from ..types import BaseUI
from ..channels import UIChannel


class CLI(BaseUI):
    mode = 'cli'

    @inject
    def __init__(
            self,
            arguments: ArgumentsSchema = CoreContainer.arguments,
            settings: SettingsSchema = CoreContainer.settings
    ):
        self._arguments: ArgumentsSchema = arguments
        self._settings: SettingsSchema = settings

        logger.info('CLI initialized')
        UIChannel.ui_initialized.publish()

    async def run(self):
        pass
