import asyncio
import websockets

from app.session import ClientSession
from app.utils import observer


class LocalServer:
    ev = observer.Event()

    def __init__(self):
        self._connected = set()
        self.ev()

    async def _handle_connection(self, connection):
        session = ClientSession(
            connection=connection
        )
        self._connected.add(session)

        async for message in connection:
            print(message)

    @property
    def connected(self) -> set[ClientSession]:
        return self._connected

    async def run(self):
        await self.ev()
        async with websockets.serve(self._handle_connection, 'localhost', 8001):
            await asyncio.Future()
