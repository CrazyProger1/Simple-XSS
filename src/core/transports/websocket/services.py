from src.utils import di
from src.core.enums import Protocol
from .dependencies import WebsocketTransportDependencyContainer
from ..services import BaseTransportService
from ..servers import BaseServer


class WebsocketTransportService(BaseTransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    def __init__(self):
        self._sessions = {}

    @di.inject
    async def run(
            self,
            host: str, port: int,
            server: BaseServer = WebsocketTransportDependencyContainer.server
    ) -> BaseServer:
        await server.run(
            host=host,
            port=port
        )
        self._sessions[(host, port)] = server
        return server

    async def stop(self, host: str, port: int):
        session = self._sessions.get((host, port))
        if session:
            await session.stop()
