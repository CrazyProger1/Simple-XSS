import flet as ft

from src.utils import di, clsutils
from src.core import settings
from src.core.settings.dependencies import current_settings_dependency
from src.core.ui.base import BaseUI
from src.core.enums import GraphicMode
from src.core.events import async_mode_entered
from src.core.context.events import (
    context_changed
)
from src.core.config import (
    MIN_RESOLUTION,
    APP,
    VERSION
)

from .components import CustomControl
from .events import (
    gui_terminated,
    gui_initialized
)
from .dependencies import (
    main_page_dependency,
    main_box_dependency,
    configurate_gui_dependencies
)
from ..events import ui_process_activated


class GUI(BaseUI):
    mode = GraphicMode.GUI

    def __init__(self):
        ui_process_activated.add_listener(self._save_controls_data)
        context_changed.add_listener(self._update_controls)
        configurate_gui_dependencies()
        gui_initialized()

    @staticmethod
    async def _save_controls_data():
        for control in clsutils.iter_instances(CustomControl):
            control.save_data()

    @staticmethod
    def _setup_controls():
        for control in clsutils.iter_instances(CustomControl):
            control.setup_data()

    @staticmethod
    def _update_controls():
        for control in clsutils.iter_instances(CustomControl):
            control.update_data()

    @di.injector.inject
    async def _display_main_box(self, page: ft.Page = main_page_dependency, box: CustomControl = main_box_dependency):
        await page.add_async(box.build())

    @di.injector.inject
    async def _configurate_main_page(
            self,
            page: ft.Page = main_page_dependency,
            sets: settings.DefaultSettingsScheme = current_settings_dependency):
        resolution = sets.graphics.resolution
        page.theme_mode = sets.graphics.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = MIN_RESOLUTION[0]
        page.window_min_height = MIN_RESOLUTION[1]
        page.overlay.extend(CustomControl.overlay)
        page.title = f'{APP} - V{VERSION}'

    async def _main(self, page: ft.Page):
        await async_mode_entered()

        di.injector.bind(main_page_dependency, page)

        await self._configurate_main_page()

        self._setup_controls()

        await self._display_main_box()

    def run(self):
        ft.app(self._main)

        gui_terminated()
