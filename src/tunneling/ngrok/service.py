from pyngrok import ngrok

from src.enums import Protocol
from src.tunneling import TunnelingService, Session


class NgrokService(TunnelingService):
    protocols = {Protocol.HTTP, Protocol.WEBSOCKET}
    name = 'ngrok'

    async def _create_tunnel(self, port: int):
        return ngrok.connect(port)

    async def run_websocket(self, port: int) -> Session:
        tunnel = await self._create_tunnel(port=port)
        return Session(Protocol.HTTP, port, tunnel.public_url.replace('https', 'wss'))

    async def run_http(self, port: int) -> Session:
        tunnel = await self._create_tunnel(port=port)
        return Session(Protocol.HTTP, port, tunnel.public_url)

    async def run(self, protocol: str | Protocol, port: int) -> Session:
        match protocol:
            case Protocol.HTTP.value:
                return await self.run_http(port=port)
            case Protocol.WEBSOCKET.value:
                return await self.run_websocket(port=port)

    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
