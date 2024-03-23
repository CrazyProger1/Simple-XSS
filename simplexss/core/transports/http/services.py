from simplexss.core.types import (
    BaseHook,
    BasePayload
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
    ) -> Session:
        pass

    async def stop(self, session: Session):
        pass
