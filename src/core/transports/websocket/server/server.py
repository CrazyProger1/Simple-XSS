import asyncio
from typing import Callable

import websockets
from typeguard import typechecked

from src.utils import di
from .dependencies import WebsocketServerDependencyContainer
from ..encoders import BaseEncoder
from ..schemes import WebsocketClient, WebsocketEvent
from ...exceptions import AddressInUseError, ServerAlreadyRunningError
from ...schemes import BaseClient, BaseEvent
from ...servers import BaseServer


class WebsocketServer(BaseServer):
    @di.inject
    def __init__(self, encoder: BaseEncoder = WebsocketServerDependencyContainer.encoder):
        self._encoder = encoder
        self._running = False
        self._host = None
        self._port = None

        self._listeners = []
        self._clients = {}

    def _authenticate(self, connection) -> BaseClient:
        client = WebsocketClient(
            origin=connection.origin,
        )
        self._clients[connection] = client
        return client

    async def _call_listeners(self, client: BaseClient, event: BaseEvent):
        for listener in self._listeners:
            try:
                asyncio.create_task(listener(self, client, event))
            except Exception as e:
                print(type(e), e)

    async def _handle_message(self, client: BaseClient, message: str):
        try:
            event = self._encoder.decode(raw=message, scheme=WebsocketEvent)
            await self._call_listeners(client=client, event=event)
        except ValueError:
            pass

    async def _handle_connection(self, connection):
        client = self._authenticate(connection=connection)
        try:
            async for message in connection:
                await self._handle_message(message=message, client=client)
        except websockets.ConnectionClosedError:
            pass

    def _get_connection(self, client: BaseClient):
        for connection, cli in self._clients.items():
            if cli == client:
                return connection

        raise

    async def _mainloop(self):
        try:
            async with websockets.serve(self._handle_connection, self._host, self._port) as server:
                while self._running:
                    await asyncio.sleep(1)

                server.close(close_connections=True)
        except OSError:
            raise AddressInUseError(
                host=self._host,
                port=self._port
            )

    @typechecked
    async def send(self, client: WebsocketClient, event: BaseEvent):
        connection = self._get_connection(client=client)
        raw = self._encoder.encode(event)
        await connection.send(raw.encode('utf-8'))

    @typechecked
    def add_listener(self, callback: Callable[["BaseServer", BaseClient, BaseEvent], any]):
        self._listeners.append(callback)

    @typechecked
    async def run(self, host: str, port: int):
        if self._running:
            raise ServerAlreadyRunningError()
        self._running = True
        self._host = host
        self._port = port
        asyncio.create_task(self._mainloop())

    async def stop(self):
        self._running = False
