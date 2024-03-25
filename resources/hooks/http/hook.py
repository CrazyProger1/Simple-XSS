from simplexss.api.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default HTTP hook, uses script src.'
    NAME = 'Default HTTP Hook'
    VERSION = '0.0.1'
    TRANSPORTS = (
        'Default HTTP Transport',
    )

    @property
    def hook(self) -> str:
        pass
