from pydantic import BaseModel

from src.utils import di

from .schemes import DefaultSettingsScheme

settings_scheme_dependency = di.Dependency(BaseModel, default=DefaultSettingsScheme)
current_settings_dependency = di.Dependency(BaseModel)
