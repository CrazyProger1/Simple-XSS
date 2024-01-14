from typeguard import typechecked

from src.utils import clsutils
from src.core.enums import GraphicMode
from src.core.config import DEFAULT_GRAPHIC_MODE
from .types import BaseUI, BaseUIFactory


class UIFactory(BaseUIFactory):
    @classmethod
    def get_modes(cls) -> set[int]:
        modes = set()
        for subcls in clsutils.iter_subclasses(BaseUI):
            mode = getattr(subcls, 'mode', None)
            if mode is not None:
                modes.add(mode)

        return modes

    @classmethod
    @typechecked
    def create_ui(cls, mode: GraphicMode | int) -> BaseUI:
        if mode not in cls.get_modes():
            mode = DEFAULT_GRAPHIC_MODE
        for subcls in clsutils.iter_subclasses(BaseUI):
            if getattr(subcls, 'mode', None) == mode:
                return subcls()
