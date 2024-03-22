from abc import (
    ABC,
    abstractmethod
)


class BaseUI(ABC):
    mode: str

    @abstractmethod
    async def run(self): ...


class BaseUIFactory(ABC):
    @abstractmethod
    def create(self, mode: str) -> BaseUI: ...

    @abstractmethod
    def get_ui(self, mode: str) -> type[BaseUI] | None: ...
