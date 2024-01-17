import flet as ft

from src.core.config import (
    MIN_RESOLUTION,
    VERSION,
    APP
)
from src.core.data import (
    DataDependencyContainer,
    Context
)
from src.core.enums import GraphicMode
from src.utils import di
from .components import BaseComponentManager
from .dependencies import (
    configure_gui_dependencies,
    GUIDependencyContainer
)
from .events import GUIEventChannel
from ..types import BaseUI


class GUI(BaseUI):
    mode = GraphicMode.GUI

    def __init__(self):
        configure_gui_dependencies()
        GUIEventChannel.gui_initialized()

    @di.inject
    async def _init_page(
            self,
            page: ft.Page,
            context: Context = DataDependencyContainer.context,
            manager: BaseComponentManager = GUIDependencyContainer.component_manager
    ):
        di.bind(GUIDependencyContainer.main_page, page)

        graphic_settings = context.settings.graphics.unwrap()
        resolution = graphic_settings.resolution
        page.theme_mode = graphic_settings.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = MIN_RESOLUTION[0]
        page.window_min_height = MIN_RESOLUTION[1]
        page.title = f'{APP} - V{VERSION}'

        GUIEventChannel.page_initialized()

        await page.update_async()
        await manager.show(page=page)

    async def run(self):
        await ft.app_async(self._init_page)
        GUIEventChannel.gui_terminated()
