from abc import ABC, abstractmethod
from typing import Callable

from .schemes import BaseClient, BaseEvent


class BaseServer(ABC):
    @abstractmethod
    async def send(self, client: BaseClient, event: BaseEvent): ...

    @abstractmethod
    def add_listener(self, callback: Callable[["BaseServer", BaseClient, BaseEvent], any]): ...

    @abstractmethod
    async def run(self, host: str, port: int): ...

    @abstractmethod
    async def stop(self): ...
