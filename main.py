from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.environment import Environment
from app.server import DefaultLocalServer

# env = Environment('wss://test')
# hook = DefaultHook.load('hooks/default', env)
# payload = DefaultPayload.load('payloads/hello_world', env)
#
# print(hook)
# print(hook.metadata.author)
#
# print(payload)
# print(payload.metadata.author)
import asyncio

serv = DefaultLocalServer()

asyncio.run(serv.run())
