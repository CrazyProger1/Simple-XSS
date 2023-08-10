import asyncio
from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.environment import Environment
from app.server import DefaultWebsocketServer
from app.tunneling import HTTPTunnelingAppWrapper
from app.session import ClientSession


async def on_client_connected(session: ClientSession):
    payload = DefaultPayload.load('payloads/chat', environment=env)
    session.environment = env
    session.payload = payload
    session.hook = hook
    await session.connection.send(
        str(
            payload
        )
    )


env = Environment()
t = HTTPTunnelingAppWrapper.get_wrapper('ngrok')('localhost', 4444)
asyncio.run(t.run())
env.public_url = t.public_url.replace('https://', 'wss://')
hook = DefaultHook.load('hooks/default', env)
print(hook)
DefaultWebsocketServer.client_connected.add_listener(on_client_connected)

asyncio.run(DefaultWebsocketServer('localhost', 4444).run())
