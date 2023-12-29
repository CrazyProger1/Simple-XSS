import flet as ft
from src.enums import GraphicMode
from src.view.launchers import BaseLauncher
from src.events import application_launched


class GUILauncher(BaseLauncher):
    mode = GraphicMode.GUI

    def __init__(self):
        pass

    async def _main(self, page):
        await application_launched()

    def launch(self):
        ft.app(target=self._main)
