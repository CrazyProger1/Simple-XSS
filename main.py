# from src.core import run
#
# if __name__ == '__main__':
#     run()

import asyncio
from src.core.transports.websocket.services import WebsocketTransportService
from src.core.transports.schemes import BaseEventScheme

ws_transport = WebsocketTransportService()


async def test(connection, event):
    await connection.send(BaseEventScheme(event='hahaha', data={}))


async def main():
    session = await ws_transport.run('localhost', 4444)
    session.add_listener(test)

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
