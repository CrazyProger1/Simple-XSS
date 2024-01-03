import flet as ft

from src.utils import di
from src.core.dependencies import current_settings
from src.core.services import settings
from src.core.ui.base import BaseUI
from src.core.enums import GraphicMode
from src.core.events import async_mode_entered
from src.core.config import MIN_RESOLUTION
from .components import CustomControl
from .events import (
    gui_terminated,
    gui_initialized
)
from .dependencies import (
    main_page,
    main_box,
    configurate_gui_dependencies
)


class GUI(BaseUI):
    mode = GraphicMode.GUI

    def _initialize(self):
        configurate_gui_dependencies()

    @di.injector.inject
    async def _display_main_box(self, page: ft.Page = main_page, box: CustomControl = main_box):
        await page.add_async(box.build())

    @di.injector.inject
    async def _configurate_main_page(
            self,
            page: ft.Page = main_page,
            sets: settings.DefaultSettingsScheme = current_settings):
        resolution = sets.graphics.resolution
        page.theme_mode = sets.graphics.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = MIN_RESOLUTION[0]
        page.window_min_height = MIN_RESOLUTION[1]
        page.overlay.extend(CustomControl.overlay)

    async def _main(self, page: ft.Page):
        await async_mode_entered()
        di.injector.bind(main_page, page)
        await self._configurate_main_page()
        await self._display_main_box()

    def run(self):
        self._initialize()
        gui_initialized()
        ft.app(self._main)
        gui_terminated()
