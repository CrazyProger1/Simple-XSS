from src.utils import di

from .contexts import Context
from .environment import Environment
from src.core.settings import SettingsDependencyContainer


class DataDependencyContainer(di.DeclarativeContainer):
    context: object = di.Singleton(
        Context,
        settings=SettingsDependencyContainer.current_settings
    )
    environment = di.Singleton(
        Environment,
        settings=SettingsDependencyContainer.current_settings,
    )
