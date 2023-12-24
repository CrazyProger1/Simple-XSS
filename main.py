import asyncio

from src.arguments import DefaultArgumentsSchema
from src.utils.arguments import SchemedArgumentParser
from src.tunneling.serveo import ServeoService
from src.tunneling.ngrok import NgrokService


async def main():
    parser = SchemedArgumentParser(schema=DefaultArgumentsSchema)
    print(parser.parse_typed_args())

    service = NgrokService()

    session = await service.run('http', 4444)
    print(session.public_url)
    await asyncio.sleep(10)
    print('STOP')
    await service.stop(session)

    await asyncio.sleep(50)


if __name__ == '__main__':
    asyncio.run(main())
