from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from ..types import BaseUI


class CLI(BaseUI):
    mode = 'cli'

    def __init__(self):
        self._arguments: ArgumentsSchema | None = None
        self._settings: SettingsSchema | None = None

    def bind_dependencies(self, **kwargs):
        pass

    async def run(self):
        pass
