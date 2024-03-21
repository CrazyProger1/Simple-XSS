import flet as ft

from simplexss.core.logging import logger
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from simplexss.core.config import (
    APP,
    VERSION,
    MIN_RESOLUTION,

)

from .containers import GUIContainer
from ..types import BaseUI
from ..channels import UIChannel


class GUI(BaseUI):
    mode = 'gui'

    def __init__(self, ):
        self._arguments: ArgumentsSchema | None = None
        self._settings: SettingsSchema | None = None

        logger.info('GUI initialized')
        UIChannel.ui_initialized.publish()

    def bind_dependencies(self, **kwargs):
        self._arguments = kwargs.get('arguments')
        self._settings = kwargs.get('settings')

        GUIContainer.arguments.bind(self._arguments)
        GUIContainer.settings.bind(self._settings)

    async def _init_page(self, page: ft.Page):
        GUIContainer.main_page.bind(page)

        graphic_settings = self._settings.graphics
        resolution = graphic_settings.resolution
        page.theme_mode = graphic_settings.theme
        page.window_width = resolution[0]
        page.window_height = resolution[1]
        page.window_min_width = MIN_RESOLUTION[0]
        page.window_min_height = MIN_RESOLUTION[1]
        page.title = f'{APP} - V{VERSION}'

        await page.add_async(GUIContainer.main_box.value.build())
        await page.update_async()

    async def run(self):
        await ft.app_async(self._init_page)

        logger.info('GUI terminated')
        await UIChannel.ui_terminated.publish_async()
