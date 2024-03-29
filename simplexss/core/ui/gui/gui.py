import flet as ft

from simplexss.core.containers import CoreContainer
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
from simplexss.utils.di import inject
from .channels import GUIChannel
from .containers import GUIContainer
from ..types import BaseUI
from ..channels import UIChannel


class GUI(BaseUI):
    mode = 'gui'

    @inject
    def __init__(
            self,
            arguments: ArgumentsSchema = CoreContainer.arguments,
            settings: SettingsSchema = CoreContainer.settings
    ):
        self._arguments: ArgumentsSchema = arguments
        self._settings: SettingsSchema = settings

        logger.info('GUI initialized')
        UIChannel.ui_initialized.publish()

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

        manager = GUIContainer.gui_manager.value
        await manager.show()

    async def update(self):
        await GUIChannel.need_update.publish_async()

    async def run(self):
        await ft.app_async(self._init_page, )

        logger.info('GUI terminated')
        await UIChannel.ui_terminated.publish_async()
