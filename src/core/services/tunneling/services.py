from abc import ABC, abstractmethod
from functools import cache

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


def get_available_tunneling_service_names(protocol: Protocol) -> set[str]:
    names = set()
    for subcls in clsutils.iter_subclasses(BaseTunnelingService):
        if protocol in subcls.protocols:
            names.add(subcls.name)
    return names




@cache
def get_tunneling_service(name: str, protocol: Protocol) -> type[BaseTunnelingService]:
    for subcls in clsutils.iter_subclasses(BaseTunnelingService):
        if name == subcls.name and protocol in subcls.protocols:
            return subcls
