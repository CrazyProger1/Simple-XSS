import flet as ft

from .constants import (
    WARNING_BANNER_ICON,
    WARNING_BANNER_BG_COLOR,
    WARNING_BANNER_TEXT_COLOR,
    WARNING_BANNER_ICON_COLOR
)
from ..types import CustomBanner
from ...enums import Messages


class WarningBanner(CustomBanner):

    def __init__(self):
        super(WarningBanner, self).__init__(
            bgcolor=WARNING_BANNER_BG_COLOR,
            leading=ft.Icon(WARNING_BANNER_ICON, color=WARNING_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, style=ft.ButtonStyle(color=WARNING_BANNER_TEXT_COLOR), on_click=self._hide),
            ],
        )

    async def _hide(self, _):
        await self.hide()

    async def show(self, page: ft.Page, message: str):
        page.banner = self
        self.content = ft.Text(message, color=WARNING_BANNER_TEXT_COLOR, selectable=True)
        page.banner.open = True
        await page.update_async()
