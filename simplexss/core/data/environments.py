from dataclasses import dataclass

from simplexss.core.schemas import (
    SettingsSchema,
    ArgumentsSchema,
)


@dataclass
class Environment:
    url: str = None
    settings: SettingsSchema = None
    arguments: ArgumentsSchema = None
