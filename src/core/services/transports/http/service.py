from ..services import BaseTransportService
from ..connections import Connection
from src.core.enums import Protocol


class HTTPTransportService(BaseTransportService):
    name = 'http'
    protocol = Protocol.HTTP

    async def run(self, host: str, port: int) -> Connection:
        pass

    async def stop(self, connection: Connection):
        pass
