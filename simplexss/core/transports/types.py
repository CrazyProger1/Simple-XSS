from abc import (
    ABC,
    abstractmethod
)
from typing import Iterable

from simplexss.core.types import (
    BaseHook,
    BasePayload
)
from .sessions import Session


class BaseTransportService(ABC):
    name: str
    protocol: str

    @abstractmethod
    async def run(
            self,
            host: str,
            port: int,
            hook: BaseHook,
            payload: BasePayload,
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
