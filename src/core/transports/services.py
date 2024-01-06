from abc import ABC, abstractmethod

from src.core.enums import Protocol
from .connections import Connection


class BaseTransportService(ABC):
    name: str
    protocol: Protocol

    @abstractmethod
    async def run(self, host: str, port: int) -> Connection: ...

    @abstractmethod
    async def stop(self, connection: Connection): ...

