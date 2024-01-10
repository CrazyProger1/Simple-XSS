from pydantic import BaseModel

from src.utils import di

settings_scheme_dependency = di.Dependency(BaseModel)
current_settings_dependency = di.Dependency(BaseModel)
