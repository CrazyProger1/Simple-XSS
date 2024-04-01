import asyncio
import subprocess

from simplexss.core.logging import logger
from simplexss.utils.network import (
    change_protocol,
    validate_port,
)

from .sessions import ServeoSession
from ..types import (
    BaseTunnelingService,
    BaseSession,
)
from ..exceptions import (
    TunnelingError
)


class ServeoService(BaseTunnelingService):
    NAME = 'serveo'
    PROTOCOLS = {
        'http',
    }
    PROTOCOL_SCHEMAS = {
        'http': 'https'
    }

    def __init__(self):
        self._processes = {}

    async def _create_tunnel(self, port: int) -> str:
        command = f'ssh -R 80:localhost:{port} serveo.net'
        process = subprocess.Popen(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False
        )
        await asyncio.sleep(3)
        try:
            out = process.stdout.readline().decode('utf-8').strip()
            public_url = out.split(' from ')[1]
            self._processes.update({public_url: process})
            logger.debug(f'Tunnel is up: localhost:{port} -> {public_url}')
        except Exception as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise TunnelingError(f'Failed to open tunnel: {e.__class__.__name__}: {e}')

        return public_url

    async def _create_session(self, port: int, protocol: str) -> BaseSession:

        schema = self.PROTOCOL_SCHEMAS[protocol]
        public_url = await self._create_tunnel(port=port)
        return ServeoSession(
            protocol=protocol,
            port=port,
            public_url=change_protocol(public_url, schema)
        )

    async def run(self, protocol: str, port: int) -> BaseSession:
        if protocol not in self.PROTOCOLS:
            raise ValueError(f'Protocol {protocol} not supported')

        validate_port(port=port, raise_exceptions=True)

        return await self._create_session(port=port, protocol=protocol)

    async def stop(self, session: BaseSession):
        process = self._processes.pop(session.public_url, None)
        if process is not None:
            process.kill()
            logger.debug(f'Tunnel is down: localhost:{session.port} -> {session.public_url}')
