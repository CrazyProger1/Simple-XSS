from src.utils import di
from src.settings import DefaultSettingsSchema
from src.arguments import DefaultArgumentsSchema

injector = di.Injector()

current_settings = di.Dependency(DefaultSettingsSchema)
current_arguments = di.Dependency(DefaultArgumentsSchema)