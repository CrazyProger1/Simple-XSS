import flet as ft

from src.enums import GraphicMode
from src.settings.dependencies import current_settings
from src.settings.schemes import DefaultSettingsScheme
from src.core.view.ui import BaseUI
from src.utils import di
from src.core.config import APP, VERSION
from .events import gui_initialized
from .di import configurate_ui_dependencies
from .dependencies import main_box, current_page
from .controls import CustomControl
from .config import WINDOW_MIN_SIZE


class GUI(BaseUI):
    mode = GraphicMode.GUI

    def __init__(self):
        configurate_ui_dependencies()

    @di.injector.inject
    def _configurate_page(self, page: ft.Page = current_page, settings: DefaultSettingsScheme = current_settings):
        page.title = f'{APP} V{VERSION}'
        resolution = settings.graphics.resolution
        page.theme_mode = settings.graphics.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = WINDOW_MIN_SIZE[0]
        page.window_min_height = WINDOW_MIN_SIZE[1]
        page.overlay.extend(CustomControl.overlay)

    @di.injector.inject
    async def _launch(self, page: ft.Page, box: CustomControl = main_box):
        di.injector.bind(current_page, page)
        self._configurate_page()
        await gui_initialized()
        await page.add_async(box.build())

    def launch(self):
        ft.app(self._launch)
