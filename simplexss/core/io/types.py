from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Sequence, Coroutine

type Sink = Callable[[str, Color], Coroutine]
type Source = Callable[[str, Color], Coroutine]


class Color(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    DEFAULT = 'default'


class BaseIOManagerAPI(ABC):
    @abstractmethod
    async def print(self, *args, color: Color | str = Color.DEFAULT, sep: str = ' ', end: str = '\n'): ...

    @abstractmethod
    async def input(self, prompt: str, /, *, color: Color | str = Color.DEFAULT): ...

    @abstractmethod
    def add_sink(self, sink: Sink): ...

    @abstractmethod
    def set_source(self, source: Source): ...
