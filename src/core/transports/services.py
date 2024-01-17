from abc import ABC, abstractmethod

from src.core.enums import Protocol
from .servers import BaseServer


class BaseTransportService(ABC):
    name: str
    protocol: Protocol

    @abstractmethod
    async def run(self, host: str, port: int) -> BaseServer: ...

    @abstractmethod
    async def stop(self, session: BaseServer): ...
