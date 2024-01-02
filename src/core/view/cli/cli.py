import asyncio

from src.enums import GraphicMode
from src.core.view.ui import BaseUI
from .events import cli_initialized


class CLI(BaseUI):
    mode = GraphicMode.CLI

    def __init__(self):
        pass

    async def _launch(self):
        print('CLI Launched')
        await cli_initialized()

    def launch(self):
        asyncio.run(self._launch())
