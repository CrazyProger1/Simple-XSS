from pydantic import BaseModel

from src.utils import di

from .schemes import DefaultSettingsScheme


class SettingsDependencyContainer(di.DeclarativeContainer):
    settings_scheme: BaseModel = DefaultSettingsScheme
    current_settings: BaseModel
