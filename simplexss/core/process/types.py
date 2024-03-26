from abc import (
    ABC,
    abstractmethod
)


class BaseProcessor(ABC):
    @abstractmethod
    async def run(self): ...

    @abstractmethod
    async def stop(self): ...
