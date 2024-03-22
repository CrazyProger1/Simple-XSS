from typing import Container
from abc import (
    ABC,
    abstractmethod
)

from simplexss.utils.packages import Package


class BaseCore(ABC):
    @abstractmethod
    async def run(self): ...


class BaseHook(Package, ABC):
    TRANSPORT: str = ''

    @property
    @abstractmethod
    def hook(self) -> str: ...


class BasePayload(Package):
    TRANSPORTS: Container[str] = set()


class BasePlugin(Package):
    pass
