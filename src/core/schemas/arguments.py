from pydantic import BaseModel, Field

from src.core.config import (
    DEFAULT_GRAPHIC_MODE,
    DEFAULT_LANGUAGE,
    SETTINGS_FILE,
)
from src.core.enums import GraphicMode


class ArgumentsSchema(BaseModel):
    settings_file: str = Field(SETTINGS_FILE, description="settings file path")
    graphic_mode: GraphicMode = Field(DEFAULT_GRAPHIC_MODE, description="graphic mode")
    language: str = Field(DEFAULT_LANGUAGE, description="language")
