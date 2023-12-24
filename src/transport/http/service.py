from src.transport import TransportService, Connection
from src.enums import Protocol


class HTTPTransportService(TransportService):
    name = 'http'
    protocol = Protocol.HTTP

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
