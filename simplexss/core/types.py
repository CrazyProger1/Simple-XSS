from typing import Container
from abc import (
    ABC,
    abstractmethod
)

from simplexss.core.io import BaseIOManagerAPI
from simplexss.core.transports import BaseTransportAPI
from simplexss.core.data import Environment
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
    environment: Environment = None

    @property
    @abstractmethod
    def payload(self) -> str: ...

    def bind_dependencies(self, **deps):
        self.transport = deps.get('transport')
        self.io = deps.get('io')
        self.environment = deps.get('env')

    def bind_endpoints(self):
        pass


class BasePlugin(Package):
    pass
