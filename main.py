import asyncio


async def main():
    pass
    # service = ServeoService()
    #
    # session = await service.run(Protocol.WEBSOCKET, 4444)
    # print(session.public_url)
    # await asyncio.sleep(30)
    # print('STOP')
    # await service.stop(session)
    #
    # await asyncio.sleep(50)


if __name__ == '__main__':
    asyncio.run(main())
