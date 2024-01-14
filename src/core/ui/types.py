from abc import ABC, abstractmethod
from src.core.enums import GraphicMode


class BaseUI(ABC):
    mode: GraphicMode | int

    @abstractmethod
    async def run(self): ...


class BaseUIFactory(ABC):
    @classmethod
    @abstractmethod
    def get_modes(cls) -> set[int]:
        pass

    @classmethod
    @abstractmethod
    def create_ui(cls, mode: GraphicMode | int) -> BaseUI: ...
