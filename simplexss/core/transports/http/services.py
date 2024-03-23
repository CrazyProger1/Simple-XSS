from simplexss.core.api import (
    BaseTransport,
)

from ..sessions import Session
from ..types import BaseTransportService


class HttpService(BaseTransportService):
    NAME = 'Default HTTP Transport'
    PROTOCOL = 'http'

    async def run(
            self,
            host: str,
            port: int,
            api: BaseTransport,
    ) -> Session:
        pass

    async def stop(self, session: Session):
        pass
