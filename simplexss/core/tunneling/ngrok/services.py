from pyngrok import (
    ngrok,
    exception as ngexception
)
from simplexss.core.logging import logger
from simplexss.utils.network import (
    change_protocol,
    validate_port,
)
from ..sessions import Session
from ..types import BaseTunnelingService
from ..exceptions import (
    TunnelingError
)


class NgrokService(BaseTunnelingService):
    name = 'ngrok'
    protocols = {
        'websocket',
    }
    protocol_schemas = {
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

    async def _create_session(self, port: int, protocol: str) -> Session:
        schema = self.protocol_schemas[protocol]
        public_url = await self._create_tunnel(port=port)
        return Session(
            protocol=protocol,
            port=port,
            public_url=change_protocol(public_url, schema)
        )

    async def run(self, protocol: str, port: int) -> Session:
        if protocol not in self.protocols:
            raise ValueError(f'Protocol {protocol} not supported')

        validate_port(port, raise_exceptions=True)
        return await self._create_session(port=port, protocol=protocol)

    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
        logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
