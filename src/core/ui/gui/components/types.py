import flet as ft

from abc import ABC, abstractmethod

from src.core.data import Context


class CustomControl(ABC):
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def setup(self, context: Context):
        """Called after components initialized."""

    def update(self, context: Context):
        """Called when the application context changes."""

    def validate(self, context: Context) -> bool:
        """Called before process launched."""
        return True

    def save(self, context: Context):
        """Called when process launched."""

    @abstractmethod
    def build(self): ...


class CustomBanner(ft.Banner):
    @abstractmethod
    async def show(self, page: ft.Page, message: str): ...

    async def hide(self):
        self.open = False
        await self.update_async()


class BaseComponentManager(ABC):
    @abstractmethod
    async def show(self, page: ft.Page): ...
