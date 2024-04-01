from pyngrok import (
    ngrok,
    exception as ngexception
)

from simplexss.core.logging import logger
from simplexss.utils.network import (
    change_protocol,
    validate_port,
)

from .sessions import NgrokSession
from ..types import (
    BaseTunnelingService,
    BaseSession,
)
from ..exceptions import (
    TunnelingError
)


class NgrokService(BaseTunnelingService):
    NAME = 'ngrok'
    PROTOCOLS = {
        'websocket',
    }
    PROTOCOL_SCHEMAS = {
        'websocket': 'wss'
    }

    @staticmethod
    async def _create_tunnel(port: int) -> str:
        try:
            tunnel = ngrok.connect(port)
            logger.debug(f'Tunnel is up: localhost:{port} -> {tunnel.public_url}')
            return tunnel.public_url
        except ngexception.PyngrokError as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelingError(f'Failed to open tunnel: {e.__class__.__name__}: {e}')

    async def _create_session(self, port: int, protocol: str) -> BaseSession:
        schema = self.PROTOCOL_SCHEMAS[protocol]
        public_url = await self._create_tunnel(port=port)
        return NgrokSession(
            protocol=protocol,
            port=port,
            public_url=change_protocol(public_url, schema)
        )

    async def run(self, protocol: str, port: int) -> BaseSession:
        if protocol not in self.PROTOCOLS:
            raise ValueError(f'Protocol {protocol} not supported')

        validate_port(port, raise_exceptions=True)
        return await self._create_session(port=port, protocol=protocol)

    async def stop(self, session: BaseSession):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
        logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
