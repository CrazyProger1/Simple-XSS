import asyncio

from simplexss.core.transports.http.fastapi import FastAPIServer
from simplexss.core.data import Environment


async def endpoint(client, event):
    event.data = {'yest': 'helloworld!'}
    print('SEND BACK')
    return event


async def main():
    server = FastAPIServer()
    api = await server.run('localhost', 4444)
    api.bind_environment(Environment(url='http://example.com'))
    api.bind_payload('{transport}\nalert(1)')
    api.endpoint('test', endpoint)

    print('Server started')

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
