
from src.utils import di
from .schemes import DefaultSettingsScheme

settings_schema = di.Dependency(DefaultSettingsScheme)
current_settings = di.Dependency(DefaultSettingsScheme)
