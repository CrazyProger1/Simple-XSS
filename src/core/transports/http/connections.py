from collections import deque

from ..connections import BaseConnection
from .schemes import ClientScheme, EventScheme


class HTTPConnection(BaseConnection):
    def __init__(self, client: ClientScheme):
        self._client = client
        self._events = deque()

    def send(self, event: EventScheme) -> None:
        self._events.append(event)

    def pop_event(self) -> EventScheme | None:
        if len(self._events) > 0:
            return self._events.popleft()

    @property
    def client(self) -> ClientScheme:
        return self._client
