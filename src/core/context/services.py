from src.utils import di

from src.core.settings.dependencies import current_settings
from src.core.settings import save_settings

from .context import DefaultContext
from .dependencies import context_class, current_context


@di.injector.inject
def create_context(setting=current_settings,
                   context_cls: DefaultContext = context_class):
    context = context_cls(settings=setting)
    di.injector.bind(current_context, context)


@di.injector.inject
def save_context(appcontext: DefaultContext = current_context):
    save_settings(settings=appcontext.settings.unwrap())
