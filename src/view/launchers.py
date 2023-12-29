from abc import ABC, abstractmethod

from src.enums import GraphicMode


class BaseLauncher(ABC):
    mode: GraphicMode

    @abstractmethod
    def launch(self): ...


def get_launcher(mode: GraphicMode) -> type[BaseLauncher]:
    for subcls in BaseLauncher.__subclasses__():
        if subcls.mode == mode:
            return subcls
