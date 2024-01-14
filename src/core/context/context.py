from dataclasses import dataclass

from src.utils import clsutils
from src.core import settings
from .events import ContextEventChannel


@dataclass
@clsutils.observable(lambda *args, **kwargs: ContextEventChannel.context_changed())
class DefaultContext:
    """
    Application data that can be changed by any part of the program.
    On ANY change automatically calls context_changed event.
    """

    settings: settings.DefaultSettingsScheme
    process_active: bool = False
    hook_code: str = None

