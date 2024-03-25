from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Callable,
    Coroutine,
    Iterable
)

from pydantic import BaseModel
from dataclasses import dataclass

type Endpoint = Callable[[BaseClient, BaseEvent], Coroutine | BaseEvent | any | None]


@dataclass(frozen=True)
class BaseSession:
    host: str
    port: int
    api: 'BaseTransportAPI'


class BaseClient(BaseModel):
    origin: str

    @abstractmethod
    def __hash__(self) -> int: ...


class BaseEvent(BaseModel):
    name: str
    data: dict = None


class BaseTransportAPI(ABC):
    @abstractmethod
    def bind_payload(self, payload: str): ...

    @abstractmethod
    def endpoint(self, event: str, endpoint: Endpoint): ...

    @abstractmethod
    async def send_event(self, client: BaseClient, event: BaseEvent): ...


class BaseTransportService(ABC):
    NAME: str
    PROTOCOL: str

    @abstractmethod
    async def run(self, host: str, port: int, **kwargs) -> BaseSession: ...

    @abstractmethod
    async def stop(self, session: BaseSession) -> None: ...


class BaseTransportServiceFactory(ABC):
    @abstractmethod
    def create(self, name: str): ...

    @abstractmethod
    def get_service(self, name: str) -> type[BaseTransportService] | None: ...

    @abstractmethod
    def get_names(self) -> Iterable[str]: ...
