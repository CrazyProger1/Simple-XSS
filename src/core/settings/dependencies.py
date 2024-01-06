from pydantic import BaseModel

from src.utils import di

settings_scheme = di.Dependency(BaseModel)
current_settings = di.Dependency(BaseModel)
