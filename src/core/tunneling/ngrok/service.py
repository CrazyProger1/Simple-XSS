from pyngrok import ngrok, exception as ngexception
from loguru import logger
from typeguard import typechecked

from src.utils import urlutils
from src.core.enums import Protocol
from ..services import BaseTunnelingService
from ..sessions import Session
from ..exceptions import TunnelOpeningError, ProtocolNotSupportedError


class NgrokService(BaseTunnelingService):
    protocols = {Protocol.WEBSOCKET, }
    name = 'ngrok'

    @staticmethod
    async def _create_tunnel(port: int) -> ngrok.NgrokTunnel:
        try:
            tunnel = ngrok.connect(port)
            logger.debug(f'Tunnel is up: localhost:{port} -> {tunnel.public_url}')
            return tunnel
        except ngexception.PyngrokError as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelOpeningError(port=port)

    async def _create_session(self, port: int, protocol: str) -> Session:
        tunnel = await self._create_tunnel(port=port)
        return Session(Protocol.HTTP, port, urlutils.change_protocol(tunnel.public_url, protocol))

    @typechecked
    async def run_websocket(self, port: int) -> Session:
        return await self._create_session(port=port, protocol='wss')

    @typechecked
    async def run_http(self, port: int) -> Session:
        return await self._create_session(port=port, protocol='https')

    @typechecked
    async def run(self, protocol: str | Protocol, port: int) -> Session:
        if protocol not in self.protocols:
            raise ProtocolNotSupportedError(protocol=protocol)

        match protocol:
            case Protocol.HTTP.value:
                session = await self.run_http(port=port)
            case Protocol.WEBSOCKET.value:
                session = await self.run_websocket(port=port)
            case _:
                raise ProtocolNotSupportedError(protocol=protocol)
        return session

    @typechecked
    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
        logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
