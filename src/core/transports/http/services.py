from src.utils import di
from src.core.enums import Protocol
from .dependencies import HTTPTransportDependencyContainer
from ..services import BaseTransportService
from ..servers import BaseServer


class HTTPTransportService(BaseTransportService):
    name = 'http'
    protocol = Protocol.HTTP

    def __init__(self):
        self._sessions = {}

    @di.inject
    async def run(
            self,
            host: str, port: int,
            server: BaseServer = HTTPTransportDependencyContainer.server
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
