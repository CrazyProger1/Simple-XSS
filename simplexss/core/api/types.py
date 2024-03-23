from abc import (
    ABC,
    abstractmethod
)

from typing import (
    Callable,
    Coroutine,
    Sequence
)
from enum import Enum

from pydantic import BaseModel

type Endpoint = Callable[[BaseEvent], BaseResponse | Coroutine | None]
type Sink = Callable[[Sequence, Color], Coroutine]
type Source = Callable[[Sequence, Color], Coroutine]


class Color(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    DEFAULT = 'default'


class BaseIOManager(ABC):
    @abstractmethod
    async def print(self, *args, color: Color = Color.DEFAULT, sep: str = ' ', end: str = '\n'): ...

    @abstractmethod
    async def input(self, prompt: str, /, *, color: Color = Color.DEFAULT): ...

    @abstractmethod
    def add_sink(self, sink: Sink): ...

    @abstractmethod
    def add_source(self, source: Source): ...


class BaseResponse(BaseModel):
    data: dict = None


class BaseClient(BaseModel):
    origin: str


class BaseEvent(BaseModel):
    name: str
    client: BaseClient
    data: dict = None


class BaseTransport(ABC):
    @abstractmethod
    def endpoint(
            self,
            event: str,
            endpoint: Endpoint,
    ): ...

    @abstractmethod
    async def handle_event(self, event: BaseEvent) -> BaseResponse: ...
