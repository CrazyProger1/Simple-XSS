import asyncio
import websockets

from loguru import logger
from app.session import ClientSession
from app.utils import observer
from app.validators import validate_port, validate_host


class LocalWebsocketServer:
    client_connected = observer.AsyncEvent()
    client_disconnected = observer.AsyncEvent()
    message_received = observer.AsyncEvent()

    @property
    def connected(self) -> set[ClientSession]:
        raise NotImplementedError

    async def run(self):
        raise NotImplementedError


class DefaultWebsocketServer(LocalWebsocketServer):
    def __init__(self, host: str, port: int):
        validate_port(port)
        validate_host(host)
        self._host = host
        self._port = port
        self._connected = set()

    async def _handle_connection(self, connection):
        session = ClientSession(
            connection=connection
        )
        self._connected.add(session)
        logger.debug(f'Client connected: {connection.origin}')
        await self.client_connected(session=session)

        try:
            async for message in connection:
                logger.debug(f'Message received: {message}')
                await self.message_received(message=message)
        except websockets.ConnectionClosedError:
            self._connected.remove(session)
            logger.debug(f'Client disconnected: {connection.origin}')
            await self.client_disconnected(session=session)

    @property
    def connected(self) -> set[ClientSession]:
        return self._connected

    async def run(self):
        async with websockets.serve(self._handle_connection, self._host, self._port):
            logger.info(f'Server is up on {self._host}:{self._port}')
            await asyncio.Future()
