from abc import ABC, abstractmethod
from typing import Callable, Iterable

from typeguard import typechecked

from .connections import BaseClientConnection
from .schemes import BaseEventScheme

Listener = Callable[[BaseClientConnection, BaseEventScheme], any]
Filter = Callable[[BaseClientConnection, BaseEventScheme], bool]


class BaseSession(ABC):
    """Server Session"""

    @abstractmethod
    def add_listener(
            self,
            callback: Listener,
            *filters: Callable[[BaseClientConnection, BaseEventScheme], bool]
    ) -> None:
        """Add an event listener. The listener will be called when the server receives the event."""

    @property
    @abstractmethod
    def listeners(self) -> Iterable[Listener]: ...

    @property
    @abstractmethod
    def host(self): ...

    @property
    @abstractmethod
    def port(self): ...


    def __repr__(self):
        return f'<Session: {self.host}:{self.port}>'


class Session(BaseSession):
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._wrapped_listeners: list[Listener] = []

    @staticmethod
    def _filter(connection: BaseClientConnection, event: BaseEventScheme, filters: Iterable[Filter]) -> bool:
        return all(flt(connection, event) for flt in filters)

    def _wrap_listener(self, listener: Listener, filters: Iterable[Filter]) -> Listener:
        def lst(connection, event):
            if self._filter(connection=connection, event=event, filters=filters):
                return listener(connection, event)

        return lst

    @typechecked
    def add_listener(
            self,
            callback: Listener,
            *filters: Filter
    ) -> None:
        self._wrapped_listeners.append(
            self._wrap_listener(
                listener=callback,
                filters=filters
            )
        )

    @property
    def listeners(self) -> Iterable[Listener]:
        return self._wrapped_listeners.copy()

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
