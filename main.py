import asyncio

from src.utils import di
from src.hook.loaders import HookLoader, BaseHookLoader
from src.payload.loaders import PayloadLoader
from src.plugin.loaders import PluginLoader

injector = di.Injector()

injector.bind(BaseHookLoader, HookLoader())
hook = injector.get_dependency(BaseHookLoader).load('resources/hooks/http')
print(hook.DESCRIPTION)
print(hook.hook)

payload = PayloadLoader.load('resources/payloads/ip')
print(payload.DESCRIPTION)

plugin = PluginLoader.load('resources/plugins/test_plugin')
print(plugin.NAME)


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
