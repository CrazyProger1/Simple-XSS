from pyngrok import ngrok

from src.tunneling import TunnelingService, Protocol, Session


class NgrokService(TunnelingService):
    protocols = {Protocol.HTTP, }
    name = 'ngrok'

    async def run_http(self, port: int) -> Session:
        tunnel = ngrok.connect(port)
        return Session(Protocol.HTTP, port, tunnel.public_url)

    async def run(self, protocol: str | Protocol, port: int) -> Session:
        match protocol:
            case Protocol.HTTP.value:
                return await self.run_http(port=port)

    async def stop(self, session: Session):
        ngrok.disconnect(session.public_url)
        ngrok.kill()
