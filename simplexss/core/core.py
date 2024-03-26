from simplexss.core.ui import BaseUIFactory
from simplexss.core.ui.channels import UIChannel
from simplexss.core.channels import CoreChannel
from simplexss.core.logging import logger
from simplexss.core.process import BaseProcessor
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from simplexss.core.types import (
    BaseCore,
)


class Core(BaseCore):
    def __init__(
            self,
            arguments: ArgumentsSchema,
            settings: SettingsSchema,
            ui_factory: BaseUIFactory,
            processor: BaseProcessor,
    ):
        self._arguments = arguments
        self._settings = settings
        self._ui_factory = ui_factory
        self._processor = processor

        CoreChannel.core_initialized.publish()
        logger.info('Core initialized')

        UIChannel.process_launched.subscribe(self._run_process)
        UIChannel.process_terminated.subscribe(self._stop_process)

    async def _run_process(self):
        await self._processor.run()

    async def _stop_process(self):
        await self._processor.stop()

    async def run(self):
        from simplexss.core.ui import gui, cli
        ui = self._ui_factory.create(self._arguments.graphic_mode)
        await ui.run()

        await CoreChannel.core_terminated.publish_async()
        logger.info('Core terminated')
