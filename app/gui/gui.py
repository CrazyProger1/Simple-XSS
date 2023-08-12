import flet as ft
from app.app import App
from .main import main


class GUI(App):
    """Graphic User Interface"""

    async def run(self):
        ft.app(target=main, view=ft.AppView.FLET_APP if not self.args.browser else ft.AppView.WEB_BROWSER)
