from simplexss.core.types import BaseCore
from simplexss.core.ui import BaseUIFactory
from simplexss.core.channels import CoreChannel
from simplexss.core.logging import logger
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)


class Core(BaseCore):
    def __init__(
            self,
            arguments: ArgumentsSchema,
            settings: SettingsSchema,
            ui_factory: BaseUIFactory,
    ):
        self._arguments = arguments
        self._settings = settings
        self._ui_factory = ui_factory

        CoreChannel.core_initialized.publish()
        logger.info('Core initialized')

    async def run(self):
        from simplexss.core.ui import gui, cli
        ui = self._ui_factory.create(self._arguments.graphic_mode)
        await ui.run()

        await CoreChannel.core_terminated.publish_async()
        logger.info('Core terminated')
