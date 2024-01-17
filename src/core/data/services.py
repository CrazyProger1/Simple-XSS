from src.utils import di

from src.core.settings import (
    save_settings
)
from .contexts import Context
from .dependencies import DataDependencyContainer


@di.inject
def save_contexts(
        graphic_context: Context = DataDependencyContainer.context
):
    save_settings(settings=graphic_context.settings.unwrap())
