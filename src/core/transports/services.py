from abc import ABC, abstractmethod

from src.core.enums import Protocol
from .sessions import BaseSession


class BaseTransportService(ABC):
    name: str
    protocol: Protocol

    @abstractmethod
    async def run(self, host: str, port: int) -> BaseSession: ...

    @abstractmethod
    async def stop(self, session: BaseSession): ...
