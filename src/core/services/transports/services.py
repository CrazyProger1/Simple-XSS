from abc import ABC, abstractmethod
from functools import cache

from src.utils import clsutils
from src.core.enums import Protocol
from .connections import Connection


class BaseTransportService(ABC):
    name: str
    protocol: Protocol

    @abstractmethod
    async def run(self, host: str, port: int) -> Connection: ...

    @abstractmethod
    async def stop(self, connection: Connection): ...


def get_available_service_names() -> set[str]:
    names = set()
    for subcls in clsutils.iter_subclasses(BaseTransportService):
        names.add(subcls.name)
    return names


@cache
def get_transport_service(name: str) -> type[BaseTransportService]:
    for subcls in clsutils.iter_subclasses(BaseTransportService):
        if name == subcls.name:
            return subcls