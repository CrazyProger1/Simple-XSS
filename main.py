from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.environment import Environment
from app.server import DefaultWebsocketServer

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

serv = DefaultWebsocketServer('localhost', 4444)
serv2 = DefaultWebsocketServer('localhost', 4445)

loop = asyncio.new_event_loop()

loop.create_task(serv.run())
print(1)
loop.create_task(serv2.run())
print(2)
loop.run_forever()
# asyncio.run(serv.run())
# asyncio.run(serv2.run())
