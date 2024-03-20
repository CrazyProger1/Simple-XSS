from pyngrok import (
    ngrok,
    exception as ngexception
)
from simplexss.core.logging import logger
from ..sessions import Session
from ..types import BaseTunnelingService


class NgrokService(BaseTunnelingService):
    name = 'ngrok'
    protocols = {
        'websocket',
    }

    async def run(self, protocol: str, port: int) -> Session:
        pass

    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
        logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
