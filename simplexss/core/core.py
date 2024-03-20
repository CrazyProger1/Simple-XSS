from .types import BaseCore


class Core(BaseCore):
    def __init__(self, arguments, settings):
        self._arguments = arguments
        self._settings = settings

    async def run(self):
        pass
