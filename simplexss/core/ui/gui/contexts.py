from dataclasses import dataclass

from simplexss.core.schemas import (
    SettingsSchema,
    ArgumentsSchema,
)


@dataclass
class Context:
    settings: SettingsSchema
    arguments: ArgumentsSchema
    process_running: bool = False
    current_hook: str = None
