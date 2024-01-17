from src.utils import di
from src.core.enums import Protocol
from .dependencies import WebsocketTransportDependencyContainer
from ..services import BaseTransportService
from ..servers import BaseServer


class WebsocketTransportService(BaseTransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    @di.inject
    async def run(
            self,
            host: str,
            port: int,
            server: BaseServer = WebsocketTransportDependencyContainer.server
    ) -> BaseServer:
        await server.run(
            host=host,
            port=port
        )
        return server

    async def stop(self, session: BaseServer):
        await session.stop()
