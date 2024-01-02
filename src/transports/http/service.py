from src.transports.services import BaseTransportService
from src.transports.connections import Connection
from src.enums import Protocol


class HTTPTransportService(BaseTransportService):
    name = 'http'
    protocol = Protocol.HTTP

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
