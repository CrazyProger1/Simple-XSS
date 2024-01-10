from src.utils import di

from src.core.settings.dependencies import current_settings_dependency
from src.core.settings import (
    save_settings,
    DefaultSettingsScheme
)
from .context import DefaultContext
from .dependencies import (
    context_class_dependency,
    current_context_dependency
)
from .events import context_created


@di.injector.inject
def create_context(
        setting: DefaultSettingsScheme = current_settings_dependency,
        context_class: DefaultContext = context_class_dependency
):
    context = context_class(settings=setting)
    di.injector.bind(current_context_dependency, context)
    context_created()


@di.injector.inject
def save_context(context: DefaultContext = current_context_dependency):
    save_settings(settings=context.settings.unwrap())
