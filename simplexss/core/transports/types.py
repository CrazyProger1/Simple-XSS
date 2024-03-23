from abc import (
    ABC,
    abstractmethod
)
from typing import Iterable

from simplexss.core.api import (
    BaseTransport,
)
from .sessions import Session


class BaseTransportService(ABC):
    NAME: str
    PROTOCOL: str

    @abstractmethod
    async def run(
            self,
            host: str,
            port: int,
            api: BaseTransport,
    ) -> Session: ...

    @abstractmethod
    async def stop(self, session: Session): ...


class BaseTransportServiceFactory(ABC):
    @abstractmethod
    def create(self, name: str): ...

    @abstractmethod
    def get_service(self, name: str) -> type[BaseTransportService] | None: ...

    @abstractmethod
    def get_names(self) -> Iterable[str]: ...
