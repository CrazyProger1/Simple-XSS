from typing import Container
from abc import (
    ABC,
    abstractmethod
)

from simplexss.utils.packages import Package
from simplexss.core.io import BaseIOManagerAPI


class BaseCore(ABC):
    @abstractmethod
    async def run(self): ...


class BaseHook(Package, ABC):
    TRANSPORTS: Container[str] = set()

    @property
    @abstractmethod
    def hook(self) -> str: ...


class BasePayload(Package):
    transport = None
    io: BaseIOManagerAPI = None

    @property
    def payload(self) -> str:
        return 'alert(1)'

    def bind_transport(self, transport):
        self.transport = transport
        self.transport.bind_payload(self.payload)

    def bind_io(self, io: BaseIOManagerAPI):
        self.io = io


class BasePlugin(Package):
    pass
