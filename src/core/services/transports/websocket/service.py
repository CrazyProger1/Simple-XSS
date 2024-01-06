from ..services import BaseTransportService
from ..connections import Connection
from src.core.enums import Protocol


class WebsocketTransportService(BaseTransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
