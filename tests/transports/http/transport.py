import asyncio

from simplexss.core.transports.http.fastapi import FastAPIServer


async def test_endpoint(client, event):
    print(client, event)


async def main():
    server = FastAPIServer()
    api = await server.run('localhost', 4444)
    api.bind_payload('alert(1)')
    api.endpoint('test', test_endpoint)
    
    print('Server started')

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
