from src.utils import di

from src.core.settings import (
    save_settings
)
from .context import DefaultContext
from .dependencies import ContextDependenciesContainer


@di.inject
def save_context(context: DefaultContext = ContextDependenciesContainer.current_context):
    save_settings(settings=context.settings.unwrap())
