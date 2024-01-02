from abc import ABC, abstractmethod
from src.core.enums import GraphicMode
from src.utils import clsutils


class BaseUI(ABC):
    mode: GraphicMode

    @abstractmethod
    def run(self): ...


def get_ui(mode: GraphicMode) -> type[BaseUI]:
    for subcls in clsutils.iter_subclasses(BaseUI):
        if getattr(subcls, 'mode', None) == mode:
            return subcls
