from ..sessions import Session
from ..types import BaseTunnelingService


class ServeoService(BaseTunnelingService):
    name = 'serveo'
    protocols = {
        'http',
    }

    async def run(self, protocol: str, port: int) -> Session:
        pass

    async def stop(self, session: Session):
        pass
