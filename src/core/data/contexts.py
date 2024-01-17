from dataclasses import dataclass

from src.utils import clsutils
from src.core.settings import DefaultSettingsScheme
from .events import DataEventChannel


@dataclass
@clsutils.observable(lambda *args, **kwargs: DataEventChannel.context_changed())
class Context:
    """Application data, that can be changed by user interface."""

    settings: DefaultSettingsScheme
    process_active: bool = False
    hook_code: str = None
