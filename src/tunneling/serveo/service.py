import asyncio
import subprocess

from src.tunneling import TunnelingService, Session
from src.enums import Protocol


class ServeoService(TunnelingService):
    protocols = {Protocol.HTTP, }
    name = 'serveo'

    def __init__(self):
        self._processes = {}

    async def run_http(self, port: int) -> Session:
        serveo_command = f'ssh -R 80:localhost:{port} serveo.net'

        process = subprocess.Popen(serveo_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        await asyncio.sleep(3)
        out = process.stdout.readline().decode('utf-8').strip()
        public_url = out.split(' from ')[1]
        self._processes.update({public_url: process})
        return Session(protocol=Protocol.HTTP, port=port, public_url=public_url)

    async def run(self, protocol: str | Protocol, port: int) -> Session:
        match protocol:
            case Protocol.HTTP.value:
                return await self.run_http(port=port)

    async def stop(self, session: Session):
        process = self._processes.pop(session.public_url, None)
        if process:
            process.kill()
