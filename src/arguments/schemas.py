from pydantic import BaseModel, Field

from src.config import DEFAULT_GRAPHIC_MODE
from src.settings.config import DEFAULT_SETTINGS_FILE
from src.enums import GraphicMode


class DefaultArgumentsSchema(BaseModel):
    settings_file: str = Field(DEFAULT_SETTINGS_FILE, description='settings file path')
    graphic_mode: GraphicMode = Field(DEFAULT_GRAPHIC_MODE, description='graphic mode')
