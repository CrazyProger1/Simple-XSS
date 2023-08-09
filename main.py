from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.environment import Environment
from app.server import LocalServer

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


def test(subj):
    print(subj)


LocalServer.ev.add_listener(test, pass_subject=True)

serv = LocalServer()
serv2 = LocalServer()
