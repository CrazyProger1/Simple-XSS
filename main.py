import asyncio
from src.core import run


async def main():
    await run()


if __name__ == '__main__':
    asyncio.run(main())
