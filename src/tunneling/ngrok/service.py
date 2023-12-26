from pyngrok import ngrok, exception as ngexception
from loguru import logger
from typeguard import typechecked

from src.enums import Protocol
from src.tunneling import TunnelingService, Session
from src.tunneling.exceptions import TunnelOpeningError
from src.utils import urlutils


class NgrokService(TunnelingService):
    protocols = {Protocol.HTTP, Protocol.WEBSOCKET}
    name = 'ngrok'

    @staticmethod
    async def _create_tunnel(port: int) -> ngrok.NgrokTunnel:
        try:
            tunnel = ngrok.connect(port)
            logger.info(f'Tunnel is up: localhost:{port} -> {tunnel.public_url}')
            return tunnel
        except ngexception.PyngrokError as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelOpeningError(port=port)

    @typechecked
    async def run_websocket(self, port: int) -> Session:
        tunnel = await self._create_tunnel(port=port)
        return Session(Protocol.HTTP, port, urlutils.change_protocol(tunnel.public_url, 'wss'))

    @typechecked
    async def run_http(self, port: int) -> Session:
        tunnel = await self._create_tunnel(port=port)
        return Session(Protocol.HTTP, port, tunnel.public_url)

    @typechecked
    async def run(self, protocol: str | Protocol, port: int) -> Session:
        match protocol:
            case Protocol.HTTP.value:
                return await self.run_http(port=port)
            case Protocol.WEBSOCKET.value:
                return await self.run_websocket(port=port)

    @typechecked
    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        logger.info(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
        ngrok.kill()
