from src.utils import di

from src.core.settings import (
    save_settings,
    SettingsDependencyContainer
)
from .context import DefaultContext
from .dependencies import ContextDependenciesContainer

from .events import ContextEventChannel


@di.inject
def create_context(
        setting=SettingsDependencyContainer.current_settings,
        context_class=ContextDependenciesContainer.context_class
):
    context = context_class(settings=setting)
    di.bind(ContextDependenciesContainer.current_context, context)
    ContextEventChannel.context_created()


@di.inject
def save_context(context: DefaultContext = ContextDependenciesContainer.current_context):
    save_settings(settings=context.settings.unwrap())
