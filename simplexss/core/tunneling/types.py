from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Iterable,
    Container
)

from dataclasses import dataclass


@dataclass
class BaseSession:
    protocol: str
    port: int
    public_url: str


class BaseTunnelingService(ABC):
    NAME: str
    PROTOCOLS: Container[str] = ()

    @abstractmethod
    async def run(self, protocol: str, port: int) -> BaseSession: ...

    @abstractmethod
    async def stop(self, session: BaseSession): ...


class BaseTunnelingServiceFactory(ABC):
    @abstractmethod
    def create(self, name: str) -> BaseTunnelingService: ...

    @abstractmethod
    def get_service(self, name: str) -> type[BaseTunnelingService] | None: ...

    @abstractmethod
    def get_names(self, protocol: str) -> Iterable[str]: ...
