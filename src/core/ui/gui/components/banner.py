import flet as ft


class CustomBanner(ft.Banner):
    async def hide(self, event=None):
        self.page.banner.open = False
        await self.page.update_async()

    async def show(self):
        self.page.banner = self
        self.page.banner.open = True
        await self.page.update_async()
