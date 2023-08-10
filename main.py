import asyncio
from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.environment import Environment
from app.server import DefaultWebsocketServer
from app.tunneling import HTTPTunnelingAppWrapper
from app.session import ClientSession


async def load_payload(session: ClientSession):
    await session.connection.send(
        str(
            DefaultPayload.load('payloads/chat', environment=env)
        )
    )


env = Environment()
t = HTTPTunnelingAppWrapper.get_wrapper('ngrok')('localhost', 4444)
asyncio.run(t.run())
env.public_url = t.public_url.replace('https://', 'wss://')
print(DefaultHook.load('hooks/default', env))
DefaultWebsocketServer.client_connected.add_listener(load_payload)
asyncio.run(DefaultWebsocketServer('localhost', 4444).run())
