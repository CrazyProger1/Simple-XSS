# from src.core import run
#
# if __name__ == '__main__':
#     run()
import asyncio

from src.core.transports.http.services import HTTPTransportService
from src.core.transports.schemes import EventScheme

service = HTTPTransportService()


async def listener(connection, event):
    print(connection.client, event)
    connection.send(EventScheme(event='hellooo', data={'testr': 'testg'}))


async def main():
    session = await service.run('localhost', 4445)
    session.add_listener(listener)

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
