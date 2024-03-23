from typing import Container
from abc import (
    ABC,
    abstractmethod
)

from simplexss.utils.packages import Package
from simplexss.core.api import (
    BaseTransport,
    BaseIOManager
)


class BaseCore(ABC):
    @abstractmethod
    async def run(self): ...


class BaseHook(Package, ABC):
    PROTOCOL: str = ''

    @property
    @abstractmethod
    def hook(self) -> str: ...


class BasePayload(Package):
    PROTOCOLS: Container[str] = set()
    transport: BaseTransport = None
    io: BaseIOManager = None

    def bind_transport(self, transport: BaseTransport):
        self.transport = transport

    def bind_io(self, io: BaseIOManager):
        self.io = io

    @property
    @abstractmethod
    def payload(self) -> str: ...


class BasePlugin(Package):
    pass
