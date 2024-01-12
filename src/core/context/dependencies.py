from src.utils import di

from .context import DefaultContext


class ContextDependenciesContainer(di.DeclarativeContainer):
    context_class: type = DefaultContext
    current_context: object
