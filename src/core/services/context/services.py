from src.core.dependencies import (
    current_settings,
    current_arguments,
    context_class,
    current_context
)
from src.core.services import settings as sets

from src.utils import di
from .schemes import DefaultContext


@di.injector.inject
def create_context(
        settings: sets.DefaultSettingsScheme = current_settings,
        context_cls: type[DefaultContext] = context_class) -> DefaultContext:
    return context_cls(
        settings=settings.model_copy(),
    )


@di.injector.inject
def create_current_context(
        settings: sets.DefaultSettingsScheme = current_settings,
        context_cls: type[DefaultContext] = context_class) -> DefaultContext:
    context = create_context(
        settings=settings,
        context_cls=context_cls
    )
    di.injector.bind(current_context, context)
    return context
