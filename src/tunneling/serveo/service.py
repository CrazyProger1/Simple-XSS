import asyncio

from typeguard import typechecked
from loguru import logger

from src.tunneling import BaseTunnelingService, Session
from src.enums import Protocol
from src.utils import system
from src.tunneling.exceptions import TunnelOpeningError, ProtocolNotSupportedError


class ServeoService(BaseTunnelingService):
    protocols = {Protocol.HTTP, }
    name = 'serveo'

    def __init__(self):
        self._processes = {}

    @typechecked
    async def run_http(self, port: int) -> Session:
        if not (0 <= port <= 65535):
            raise ValueError(f'{port} is not valid port number')

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
        return Session(protocol=Protocol.HTTP, port=port, public_url=public_url)

    @typechecked
    async def run(self, protocol: str | Protocol, port: int) -> Session:
        if protocol not in self.protocols:
            raise ProtocolNotSupportedError(protocol=protocol)

        match protocol:
            case Protocol.HTTP.value:
                return await self.run_http(port=port)

    @typechecked
    async def stop(self, session: Session):
        process = self._processes.pop(session.public_url, None)
        if process:
            process.kill()
            logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
