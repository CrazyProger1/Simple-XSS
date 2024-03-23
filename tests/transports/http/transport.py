import asyncio

from simplexss.core.transports.http.server import FastAPIServer
from simplexss.core.api import APITransport, BaseResponse


async def endpoint(client, event):
    print(event)
    return BaseResponse()


async def main():
    transport = APITransport()
    transport.endpoint('test', endpoint)

    server = FastAPIServer()
    await server.run('localhost', 4444, transport)

    print('Server started')

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
