from abc import ABC, abstractmethod
from typing import Callable

from .schemes import BaseClientScheme, BaseEventScheme


class BaseClientConnection(ABC):
    """Client ClientConnection"""

    @abstractmethod
    async def send(self, event: BaseEventScheme):
        """Sends the specified event to client over the ws_connection."""

    @property
    @abstractmethod
    def client(self) -> BaseClientScheme:
        """Gets the client associated with this ws_connection."""

    def __repr__(self):
        return f'<ClientConnection: {self.client}>'


class ClientConnection(BaseClientConnection):
    def __init__(self, client: BaseClientScheme, on_send: Callable[[BaseClientConnection, BaseEventScheme], any]):
        self._client = client
        self._on_send = on_send

    async def send(self, event: BaseEventScheme):
        await self._on_send(self, event)

    @property
    def client(self) -> BaseClientScheme:
        return self._client
