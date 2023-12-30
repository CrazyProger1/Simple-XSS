from abc import ABC, abstractmethod
from functools import cache

from src.enums import GraphicMode
from src.utils import clsutils


class BaseUI(ABC):
    mode: GraphicMode

    @abstractmethod
    async def launch(self): ...


@cache
def get_ui(graphic_mode: GraphicMode) -> BaseUI:
    for subcls in clsutils.iter_subclasses(BaseUI):
        if subcls.mode == graphic_mode:
            return subcls()
