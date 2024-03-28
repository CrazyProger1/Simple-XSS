from abc import (
    ABC,
    abstractmethod
)

import flet as ft

from simplexss.core.ui.contexts import UIContext


class BaseComponent(ABC):
    context: UIContext = None
    page: ft.Page = None
    overlay = []
    components = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.components.append(instance)
        return instance

    async def setup_async(self):
        pass

    async def update_async(self):
        pass

    async def validate_async(self):
        pass

    async def save_async(self):
        pass

    @abstractmethod
    def build(self): ...


class BaseComponentManager(ABC):

    @abstractmethod
    async def show(self): ...

    @abstractmethod
    async def hide(self): ...


class BaseBanner(ft.Banner):
    @abstractmethod
    async def show(self, page: ft.Page, message: str): ...

    @abstractmethod
    async def hide(self): ...
