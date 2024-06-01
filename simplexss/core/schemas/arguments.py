from pydantic import BaseModel, Field

from simplexss.core.config import (
    DEFAULT_GRAPHIC_MODE,
    DEFAULT_LANGUAGE,
    DEFAULT_SETTINGS_FILE,
)
from simplexss.core.enums import GraphicMode


class ArgumentsSchema(BaseModel):
    settings_file: str = Field(DEFAULT_SETTINGS_FILE, description="settings file path")
    graphic_mode: GraphicMode = Field(DEFAULT_GRAPHIC_MODE, description="graphic mode")
    language: str = Field(DEFAULT_LANGUAGE, description="language")
