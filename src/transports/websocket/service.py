from src.transports import BaseTransportService, Connection
from src.enums import Protocol


class WebsocketTransportService(BaseTransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
