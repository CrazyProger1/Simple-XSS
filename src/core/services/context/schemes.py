from pydantic import BaseModel

from src.core.services import settings


class DefaultContext(BaseModel):
    """
    Application data that can be changed by any part of the program.
    It's necessary to call context_changed event when the context changes.
    """

    settings: settings.DefaultSettingsScheme
    hook: str = None
