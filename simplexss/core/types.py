from typing import Container
from abc import (
    ABC,
    abstractmethod
)

from simplexss.core.io import BaseIOManagerAPI
from simplexss.core.transports import BaseTransportAPI
from simplexss.utils.packages import Package


class BaseCore(ABC):
    @abstractmethod
    async def run(self): ...


class BaseHook(Package, ABC):
    TRANSPORTS: Container[str] = set()

    @property
    @abstractmethod
    def hook(self) -> str: ...


class BasePayload(Package):
    transport: BaseTransportAPI = None
    io: BaseIOManagerAPI = None

    @property
    def payload(self) -> str:
        return ''

    def bind_transport(self, transport: BaseTransportAPI):
        self.transport = transport
        self.transport.bind_payload(self.payload)

    def bind_io(self, io: BaseIOManagerAPI):
        self.io = io


class BasePlugin(Package):
    pass
