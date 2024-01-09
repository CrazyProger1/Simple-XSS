import inspect
from abc import ABC
from typing import Callable, Iterable

from .connections import BaseConnection
from .schemes import BaseEventScheme


class BaseSession(ABC):
    """Server API"""

    def __init__(self, host: str, port: int):
        self._listeners_filters = {}
        self._host = host
        self._port = port

    @staticmethod
    def _filter(
            connection: BaseConnection, event: BaseEventScheme,
            filters: Iterable[Callable[[BaseConnection, BaseEventScheme], bool]]
    ) -> bool:

        return all(flt(connection, event) for flt in filters)

    def add_listener(
            self,
            callback: Callable[[BaseConnection, BaseEventScheme], any],
            *filters: Callable[[BaseConnection, BaseEventScheme], bool]
    ) -> None:
        if callback not in self._listeners_filters:
            self._listeners_filters.update({callback: filters})

    async def call_listeners(self, connection: BaseConnection, event: BaseEventScheme):
        for listener, filters in self._listeners_filters.items():
            if self._filter(connection=connection, event=event, filters=filters):
                if inspect.iscoroutinefunction(listener):
                    await listener(connection, event)
                else:
                    listener(connection, event)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def __repr__(self):
        return f'<Session: {self.host}:{self.port}>'
