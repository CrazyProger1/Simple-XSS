from abc import ABC, abstractmethod
from src.core.enums import GraphicMode


class BaseUI(ABC):
    mode: GraphicMode | int

    @abstractmethod
    async def run(self): ...
