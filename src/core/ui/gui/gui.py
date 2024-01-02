import flet as ft

from src.core.ui.base import BaseUI
from src.core.enums import GraphicMode
from src.core.events import async_mode_entered


class GUI(BaseUI):
    mode = GraphicMode.GUI

    async def _main(self, page: ft.Page):
        await async_mode_entered()

    def run(self):
        ft.app(self._main)
