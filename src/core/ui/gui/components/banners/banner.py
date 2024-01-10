import flet as ft


class CustomBanner(ft.Banner):
    async def hide(self, event=None):
        self.open = False
        await self.update_async()
