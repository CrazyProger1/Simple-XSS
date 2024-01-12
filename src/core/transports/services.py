from abc import ABC, abstractmethod

from src.core.enums import Protocol


class BaseTransportService(ABC):
    name: str
    protocol: Protocol

    @abstractmethod
    async def run(self, host: str, port: int): ...

    @abstractmethod
    async def stop(self, session): ...
