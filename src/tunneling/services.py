from abc import ABC, abstractmethod

from .enums import Protocol
from .sessions import Session


class TunnelingService(ABC):
    protocols: set[str | Protocol]
    name: str

    @abstractmethod
    def run(self, protocol: str | Protocol, port: int) -> Session: ...

    @abstractmethod
    def stop(self, session: Session): ...
