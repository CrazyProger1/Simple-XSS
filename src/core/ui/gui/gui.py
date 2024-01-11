import flet as ft

from src.utils import di
from src.core.enums import GraphicMode
from src.core.context import DefaultContext
from src.core.context.dependencies import current_context_dependency
from src.core.ui.base import BaseUI
from src.core.config import (
    MIN_RESOLUTION,
    APP, VERSION
)
from .components import CustomControl

from .events import (
    gui_terminated,
    gui_initialized
)
from .dependencies import (
    configurate_gui_dependencies,
    main_page_dependency,
    main_control_dependency
)


class GUI(BaseUI):
    mode = GraphicMode.GUI

    def __init__(self):
        configurate_gui_dependencies()
        gui_initialized()

    @di.injector.inject
    async def _setup_page(
            self,
            page: ft.Page,
            control: CustomControl = main_control_dependency,
            context: DefaultContext = current_context_dependency
    ):
        di.injector.bind(main_page_dependency, page)

        graphic_settings = context.settings.graphics.unwrap()
        resolution = graphic_settings.resolution
        page.theme_mode = graphic_settings.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = MIN_RESOLUTION[0]
        page.window_min_height = MIN_RESOLUTION[1]
        page.overlay.extend(CustomControl.overlay)
        page.title = f'{APP} - V{VERSION}'

        await page.update_async()
        await page.add_async(control.build())

    async def run(self):
        await ft.app_async(self._setup_page)
        gui_terminated()
