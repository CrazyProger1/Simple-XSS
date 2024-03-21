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
            ui_factory: BaseUIFactory
    ):
        self._arguments = arguments
        self._settings = settings
        self._ui_factory = ui_factory

        CoreChannel.core_initialized.publish()
        logger.info('Core initialized')

    async def run(self):
        ui = self._ui_factory.create(self._arguments.graphic_mode)
        ui.bind_dependencies(
            arguments=self._arguments,
            settings=self._settings,
        )
        await ui.run()
        
        await CoreChannel.core_terminated.publish_async()
        logger.info('Core terminated')
