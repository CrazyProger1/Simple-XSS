import asyncio

from src.enums import GraphicMode
from src.view.launchers import BaseLauncher
from src.events import application_launched


class CLILauncher(BaseLauncher):
    mode = GraphicMode.CLI

    def __init__(self):
        pass

    async def _main(self):
        await application_launched()

    def launch(self):
        asyncio.run(self._main())
