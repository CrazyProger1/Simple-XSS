from abc import ABC, abstractmethod
from functools import cache

from typeguard import typechecked

from src.utils import clsutils
from src.core.enums import Protocol
from .sessions import Session


class BaseTunnelingService(ABC):
    protocols: set[str | Protocol]
    name: str

    @abstractmethod
    async def run(self, protocol: str | Protocol, port: int) -> Session: ...

    @abstractmethod
    async def stop(self, session: Session): ...



