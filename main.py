import asyncio

from src.core import transports, tunneling
from src.utils import di

transports.TransportsDependencyContainer.configure()
tunneling.TunnelingDependencyContainer.configure()


@di.inject
async def test(factory=transports.TransportsDependencyContainer.factory):
    service = factory.create('http')


async def main():
    await test()
    # await run()


if __name__ == '__main__':
    asyncio.run(main())
