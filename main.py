import asyncio

from src.core import transports
from src.utils import di

transports.TransportsDependencyContainer.configure()


async def listener(server, client, event):
    await server.send(client, event)


@di.inject
async def test(factory=transports.TransportsDependencyContainer.factory):
    service = factory.create('http')
    server = await service.run('localhost', 4444)
    server.add_listener(listener)

    await asyncio.sleep(100)


async def main():
    await test()


if __name__ == '__main__':
    asyncio.run(main())
