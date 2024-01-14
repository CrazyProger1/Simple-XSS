from src.api.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default HTTP hook, uses script src.'
    NAME = 'HTTP Hook'
    VERSION = '0.1'
    TRANSPORT = 'http'

    def hook(self) -> str:
        pass
