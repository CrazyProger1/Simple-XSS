from abc import ABC, abstractmethod
from typing import Callable, Collection


class BaseEventChannel(ABC):
    @classmethod
    @property
    @abstractmethod
    def events(cls) -> Collection["BaseEvent"]: ...


class BaseEvent(ABC):
    @property
    @abstractmethod
    def channel(self) -> type[BaseEventChannel]: ...

    @abstractmethod
    def subscribe(self, callback: Callable): ...

    @abstractmethod
    def publish(self, *args, **kwargs): ...


class BaseAsyncEvent(BaseEvent):
    @abstractmethod
    async def publish_async(self, *args, **kwargs): ...
