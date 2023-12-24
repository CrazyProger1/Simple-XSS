from abc import ABC, abstractmethod

from src.enums import Protocol
from .sessions import Session


class TunnelingService(ABC):
    protocols: set[str | Protocol]
    name: str

    @abstractmethod
    async def run(self, protocol: str | Protocol, port: int) -> Session: ...

    @abstractmethod
    async def stop(self, session: Session): ...
