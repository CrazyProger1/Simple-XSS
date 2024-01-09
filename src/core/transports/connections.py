from abc import ABC, abstractmethod

from .schemes import BaseClientScheme, BaseEventScheme


class BaseConnection(ABC):
    @abstractmethod
    def send(self, event: BaseEventScheme) -> None: ...

    @abstractmethod
    def pop_event(self) -> BaseClientScheme | None: ...

    @property
    @abstractmethod
    def client(self) -> BaseClientScheme: ...
