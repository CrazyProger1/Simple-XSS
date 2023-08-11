import flet as ft
from app.app import App
from .main import main


class GUI(App):
    async def run(self):
        ft.app(target=main, view=ft.AppView.FLET_APP)
