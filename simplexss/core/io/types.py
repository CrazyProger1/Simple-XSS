from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Sequence, Coroutine

type Sink = Callable[[Sequence, Color], Coroutine]
type Source = Callable[[Sequence, Color], Coroutine]


class Color(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    DEFAULT = 'default'


class BaseIOManagerAPI(ABC):
    @abstractmethod
    async def print(self, *args, color: Color = Color.DEFAULT, sep: str = ' ', end: str = '\n'): ...

    @abstractmethod
    async def input(self, prompt: str, /, *, color: Color = Color.DEFAULT): ...

    @abstractmethod
    def add_sink(self, sink: Sink): ...

    @abstractmethod
    def add_source(self, source: Source): ...
