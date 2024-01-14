from src.utils import di

from .context import DefaultContext
from src.core.settings import SettingsDependencyContainer


class ContextDependenciesContainer(di.DeclarativeContainer):
    context_class: type = DefaultContext
    current_context: object = di.Singleton(
        DefaultContext,
        settings=SettingsDependencyContainer.current_settings
    )
