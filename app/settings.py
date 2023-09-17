from config import (
    DEFAULT_HOOK,
    DEFAULT_PAYLOAD,
    DEFAULT_TUNNELING_APP,
    DEFAULT_HOST,
    DEFAULT_PORT,
    USE_TUNNELING_APP
)

from app.utils import settings


class Settings(settings.SettingsSchema):
    public_url: str = None
    payload_path: str = DEFAULT_PAYLOAD
    hook_path: str = DEFAULT_HOOK
    use_tunneling_app: bool = USE_TUNNELING_APP
    tunneling_app: str = DEFAULT_TUNNELING_APP
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
