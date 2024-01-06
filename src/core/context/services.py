from src.utils import di

from src.core.settings.dependencies import current_settings_dependency
from src.core.settings import save_settings

from .context import DefaultContext
from .dependencies import context_class_dependency, current_context_dependency


@di.injector.inject
def create_context(setting=current_settings_dependency,
                   context_cls: DefaultContext = context_class_dependency):
    context = context_cls(settings=setting)
    di.injector.bind(current_context_dependency, context)


@di.injector.inject
def save_context(appcontext: DefaultContext = current_context_dependency):
    save_settings(settings=appcontext.settings.unwrap())
