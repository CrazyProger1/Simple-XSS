from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Callable,
    Coroutine
)

from pydantic import BaseModel

type Endpoint = Callable[[BaseClient, BaseEvent], Coroutine | BaseEvent | any | None]


class BaseSession(BaseModel):
    host: str
    port: int
    api: 'BaseTransportAPI'


class BaseClient(BaseModel):
    origin: str


class BaseEvent(BaseModel):
    name: str
    data: dict = None


class BaseTransportAPI(ABC):
    @abstractmethod
    def bind_payload(self, payload: str): ...

    @abstractmethod
    def endpoint(self, event: str, endpoint: Endpoint): ...

    @abstractmethod
    def send_event(self, event: BaseEvent): ...


class BaseTransportService(ABC):
    NAME: str
    PROTOCOL: str

    @abstractmethod
    def run(self, host: str, port: int) -> BaseSession: ...

    @abstractmethod
    def stop(self, session: BaseSession) -> None: ...
