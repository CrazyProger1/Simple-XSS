import asyncio

from typeguard import typechecked
from loguru import logger

from src.core.enums import Protocol
from src.utils import system, network
from ..constants import PROTOCOL_PREFIXES
from ..services import BaseTunnelingService
from ..sessions import Session
from ..exceptions import (
    TunnelOpeningError,
    ProtocolNotSupportedError
)


class ServeoService(BaseTunnelingService):
    protocols = {Protocol.HTTP, Protocol.WEBSOCKET}
    name = 'serveo'

    def __init__(self):
        self._processes = {}

    async def _create_tunnel(self, port: int) -> str:
        command = f'ssh -R 80:localhost:{port} serveo.net'
        process = system.execute(command=command)
        await asyncio.sleep(3)
        try:
            out = process.stdout.readline().decode('utf-8').strip()
            public_url = out.split(' from ')[1]
            self._processes.update({public_url: process})
            logger.debug(f'Tunnel is up: localhost:{port} -> {public_url}')
        except Exception as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelOpeningError(port=port)

        return public_url

    async def _create_session(self, port: int, protocol: Protocol) -> Session:
        network.validate_port(port=port, raise_exceptions=True)
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
        process = self._processes.pop(session.public_url, None)
        if process:
            process.kill()
            logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
