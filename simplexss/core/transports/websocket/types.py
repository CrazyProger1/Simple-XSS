from abc import (
    ABC,
    abstractmethod
)
from simplexss.core.transports import BaseTransportAPI


class BaseWebsocketServer(ABC):
    @abstractmethod
    async def run(self, host: str, port: int) -> BaseTransportAPI: ...

    @abstractmethod
    async def stop(self): ...
