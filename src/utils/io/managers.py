from typing import Callable, Optional
from abc import ABC, abstractmethod
from typeguard import typechecked

from .enums import Color


class BaseIOManager(ABC):
    @abstractmethod
    def input(self, prompt: str = '', color: Color = Color.WHITE) -> str: ...

    @abstractmethod
    def print(self, *messages, sep: str = ' ', end: str = '\n', color: Color = Color.WHITE): ...

    def info(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.BLUE)
        self.print(*messages, **kwargs)

    def warning(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.YELLOW)
        self.print(*messages, **kwargs)

    def error(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.RED)
        self.print(*messages, **kwargs)


class IOManager(BaseIOManager):
    @typechecked
    def __init__(self, input_source: Optional[Callable] = None, print_source: Optional[Callable] = None):
        self._input_source = input_source
        self._print_source = print_source

    @property
    def print_source(self):
        return self._print_source

    @property
    def input_source(self):
        return self._input_source

    @input_source.setter
    @typechecked
    def input_source(self, source: Callable):
        self._input_source = source

    @print_source.setter
    @typechecked
    def print_source(self, source: Callable):
        self._print_source = source

    @typechecked
    def input(self, prompt: str = '', color: Color = Color.WHITE) -> str:
        if not self._input_source:
            raise TypeError('Input source not set')

        return self._input_source(prompt, color=color)

    @typechecked
    def print(self, *messages, sep: str = ' ', end: str = '\n', color: Color = Color.WHITE):
        if not self._print_source:
            raise TypeError('Print source not set')

        self._print_source(*messages, sep=sep, end=end, color=color)


class AsyncIOManager(IOManager):
    async def input(self, prompt: str = '', color: Color = Color.WHITE) -> str:
        if not self._input_source:
            raise TypeError('Input source not set')

        return await self._input_source(prompt, color=color)

    async def print(self, *messages, sep: str = ' ', end: str = '\n', color: Color = Color.WHITE):
        if not self._print_source:
            raise TypeError('Print source not set')

        await self._print_source(*messages, sep=sep, end=end, color=color)

    async def info(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.BLUE)
        await self.print(*messages, **kwargs)

    async def warning(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.YELLOW)
        await self.print(*messages, **kwargs)

    async def error(self, *messages, **kwargs):
        kwargs['color'] = kwargs.get('color', Color.RED)
        await self.print(*messages, **kwargs)
