from pydantic import BaseModel, Field

from src.core.config import DEFAULT_SETTINGS_FILE, DEFAULT_GRAPHIC_MODE


class DefaultArgumentsScheme(BaseModel):
    settings_file: str = Field(DEFAULT_SETTINGS_FILE, description='settings file path')
    graphic_mode: int = Field(DEFAULT_GRAPHIC_MODE, description='graphic mode')
