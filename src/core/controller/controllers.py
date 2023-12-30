from abc import ABC, abstractmethod
from .events import controller_initialized


class BaseController(ABC):
    @abstractmethod
    async def launch(self): ...


class Controller(BaseController):
    async def launch(self):
        await controller_initialized()
