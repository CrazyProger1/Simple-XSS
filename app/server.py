import asyncio
import websockets

from loguru import logger
from app.session import ClientSession
from app.utils import observer, clss


class LocalServer(metaclass=clss.SingletonMeta):
    client_connected = observer.AsyncEvent()
    client_disconnected = observer.AsyncEvent()
    message_received = observer.AsyncEvent()

    @property
    def connected(self) -> set[ClientSession]:
        raise NotImplementedError

    async def run(self):
        raise NotImplementedError


class DefaultLocalServer(LocalServer):
    def __init__(self):
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
        host = 'localhost'
        port = 4444
        async with websockets.serve(self._handle_connection, host, port):
            logger.info(f'Server is running on {host}:{port}')
            await asyncio.Future()
