import flet as ft

from .enums import Messages
from ..types import BaseBanner


class BannerBasicFunctionality(BaseBanner):
    TEXT_COLOR = None
    BG_COLOR = None
    ICON = None
    ICON_COLOR = None

    def __init__(self):
        super(BannerBasicFunctionality, self).__init__(
            bgcolor=self.BG_COLOR,
            leading=ft.Icon(self.ICON, color=self.ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, style=ft.ButtonStyle(color=self.TEXT_COLOR), on_click=self._hide),
            ],
        )

    async def _hide(self, _):
        await self.hide()

    async def show(self, page: ft.Page, message: str):
        page.banner = self
        self.content = ft.Text(message, color=self.TEXT_COLOR, selectable=True)
        page.banner.open = True
        await page.update_async()

    async def hide(self):
        self.open = False
        await self.update_async()
