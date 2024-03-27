from abc import (
    ABC,
    abstractmethod
)

from .contexts import Context


class BaseComponent(ABC):
    context: Context = None
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
