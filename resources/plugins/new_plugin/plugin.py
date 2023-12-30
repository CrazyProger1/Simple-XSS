from src.plugins import BasePlugin
from src.core.events import async_mode_entered


class Plugin(BasePlugin):
    AUTHOR = 'crazyproger1'
    NAME = 'Test plugin'
    VERSION = '0.1'

    def __init__(self):
        async_mode_entered.add_listener(self.on_async)

    async def on_async(self):
        print('ASYNC!')
