
from src.utils import di
from .schemas import DefaultSettingsSchema

settings_schema = di.Dependency(DefaultSettingsSchema)
current_settings = di.Dependency(DefaultSettingsSchema)
