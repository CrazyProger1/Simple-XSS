from abc import (
    ABC,
    abstractmethod
)

from simplexss.core.api import (
    BaseTransport,
)


class BaseHTTPServer(ABC):
    @abstractmethod
    async def run(self, host: str, port: int, api: BaseTransport): ...

    @abstractmethod
    async def stop(self): ...
