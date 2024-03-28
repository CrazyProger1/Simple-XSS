from dataclasses import dataclass

from simplexss.core.schemas import (
    SettingsSchema,
    ArgumentsSchema,
)


@dataclass
class UIContext:
    settings: SettingsSchema
    arguments: ArgumentsSchema
    process_running: bool = False
    hook: str = None
