import flet as ft
import payload

from app.app import App
from .main import main
from .io import GUIIOManager


class GUI(App):
    """Graphic User Interface"""

    async def run(self):
        ft.app(target=main, view=ft.AppView.FLET_APP if not self.args.browser else ft.AppView.WEB_BROWSER)
