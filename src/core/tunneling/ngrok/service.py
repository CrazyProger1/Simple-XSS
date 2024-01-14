from pyngrok import ngrok, exception as ngexception
from loguru import logger
from typeguard import typechecked

from src.utils import network
from src.core.enums import Protocol
from ..constants import PROTOCOL_PREFIXES
from ..services import BaseTunnelingService
from ..sessions import Session
from ..exceptions import (
    TunnelOpeningError,
    ProtocolNotSupportedError
)


class NgrokService(BaseTunnelingService):
    protocols = {Protocol.WEBSOCKET, Protocol.HTTP}
    name = 'ngrok'

    @staticmethod
    async def _create_tunnel(port: int) -> str:
        try:
            tunnel = ngrok.connect(port)
            logger.debug(f'Tunnel is up: localhost:{port} -> {tunnel.public_url}')
            return tunnel.public_url
        except ngexception.PyngrokError as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelOpeningError(port=port)

    async def _create_session(self, port: int, protocol: Protocol) -> Session:
        network.validate_port(port=port)
        prefix = PROTOCOL_PREFIXES[protocol]
        public_url = await self._create_tunnel(port=port)
        return Session(
            protocol=protocol,
            port=port,
            public_url=network.change_protocol(public_url, prefix)
        )

    @typechecked
    async def run(self, protocol: str | Protocol, port: int) -> Session:
        if protocol not in self.protocols:
            raise ProtocolNotSupportedError(protocol=protocol)

        return await self._create_session(port=port, protocol=protocol)

    @typechecked
    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
        logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
