from src.utils import di
from src.core.enums import Protocol
from .dependencies import HTTPTransportDependencyContainer
from ..services import BaseTransportService
from ..servers import BaseServer


class HTTPTransportService(BaseTransportService):
    name = 'http'
    protocol = Protocol.HTTP

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
        return server

    async def stop(self, session: BaseServer):
        await session.stop()
