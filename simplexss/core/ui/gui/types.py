from abc import (
    ABC,
    abstractmethod
)


class CustomControl(ABC):
    overlay = []

    @abstractmethod
    def build(self): ...
