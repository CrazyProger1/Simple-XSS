from src.transport import TransportService, Connection
from src.enums import Protocol


class WebsocketTransportService(TransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
