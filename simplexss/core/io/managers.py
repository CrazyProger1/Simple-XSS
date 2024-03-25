from .types import (
    BaseIOManager,
    Source,
    Sink,
    Color
)


class APIIOManager(BaseIOManager):
    def __init__(self):
        self._sink: Sink | None = None
        self._source: Source | None = None

    async def print(self, *args, color: Color = Color.DEFAULT, sep: str = ' ', end: str = '\n'):
        seq = sep.join(map(str, args)) + end
        return await self._sink(seq, color)

    async def input(self, prompt: str, /, *, color: Color = Color.DEFAULT):
        return await self._source(prompt, color)

    def add_sink(self, sink: Sink):
        if not callable(sink):
            raise TypeError('Sink must be callable')
        self._sink = sink

    def add_source(self, source: Source):
        if not callable(source):
            raise TypeError('Source must be callable')
        self._source = source
