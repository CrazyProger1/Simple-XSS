import asyncio

import websockets
from functools import cache

from ..connections import BaseClientConnection, ClientConnection
from ..exceptions import AddressInUseError
from ..schemes import BaseClientScheme, BaseEventScheme
from ..servers import BaseServer
from ..sessions import Session
from ..encoders import BaseEncoder, JSONEncoder


class WebsocketServer(BaseServer):
    def __init__(self, host: str, port: int, encoder: BaseEncoder = JSONEncoder):
        self._host = host
        self._port = port
        self._session = Session(host=host, port=port)
        self._running = True
        self._ws_client_pairs = {}
        self._encoder = encoder

    @property
    def session(self) -> Session:
        return self._session

    @property
    def port(self) -> int:
        return self._port

    @property
    def host(self) -> str:
        return self._host

    @cache
    def _get_ws_connection(self, client: BaseClientConnection):
        for ws, client_conn in self._ws_client_pairs.items():
            if client == client_conn:
                return ws

    async def _send_event(self, client: BaseClientConnection, event: BaseEventScheme):
        ws = self._get_ws_connection(client=client)
        raw = self._encoder.encode(event=event)
        await ws.send(raw.encode('utf-8'))

    async def _handle_event(self, client: BaseClientConnection, event: BaseEventScheme):
        for listener in self._session.listeners:
            await listener(client, event)

    async def _authenticate(self, ws_connection) -> BaseClientConnection:
        if ws_connection not in self._ws_client_pairs:
            self._ws_client_pairs[ws_connection] = ClientConnection(
                client=BaseClientScheme(origin=ws_connection.origin),
                on_send=self._send_event
            )
        return self._ws_client_pairs[ws_connection]

    async def _handle_message(self, client: BaseClientConnection, message: str):
        event = self._encoder.decode(raw=message, scheme=BaseEventScheme)
        await self._handle_event(client=client, event=event)

    async def _wait_for_message(self, ws_connection, client: BaseClientConnection):
        try:
            async for message in ws_connection:
                await self._handle_message(message=message, client=client)
        except websockets.ConnectionClosedError:
            print('ClientConnection closed')

    async def _handle_connection(self, ws_connection):
        client = await self._authenticate(ws_connection=ws_connection)
        await self._wait_for_message(ws_connection=ws_connection, client=client)

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

    async def run(self):
        asyncio.create_task(self._mainloop())

    async def stop(self):
        self._running = False
