import flet as ft

from .constants import (
    ERROR_BANNER_BG_COLOR,
    ERROR_BANNER_ICON,
    ERROR_BANNER_ICON_COLOR,
    ERROR_BANNER_TEXT_COLOR
)
from ..types import CustomBanner
from ...enums import Messages


class ErrorBanner(CustomBanner):

    def __init__(self):
        super(ErrorBanner, self).__init__(
            bgcolor=ERROR_BANNER_BG_COLOR,
            leading=ft.Icon(ERROR_BANNER_ICON, color=ERROR_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, style=ft.ButtonStyle(color=ERROR_BANNER_TEXT_COLOR), on_click=self._hide),
            ],
        )

    async def _hide(self, _):
        await self.hide()

    async def show(self, page: ft.Page, message: str):
        page.banner = self
        self.content = ft.Text(message, color=ERROR_BANNER_TEXT_COLOR, selectable=True)
        page.banner.open = True
        await page.update_async()
