from pydantic import BaseModel, Field

from src.core.config import (
    DEFAULT_RESOLUTION,
    DEFAULT_THEME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_TRANSPORT,
    DEFAULT_PAYLOADS_DIRECTORY,
    DEFAULT_HOOKS_DIRECTORY,
    DEFAULT_TUNNELING_SERVICE
)


class HookSettingsScheme(BaseModel):
    current: str = None
    directory: str = DEFAULT_HOOKS_DIRECTORY


class PayloadSettingsScheme(BaseModel):
    current: str = None
    directory: str = DEFAULT_PAYLOADS_DIRECTORY


class TransportSettingsScheme(BaseModel):
    current: str = DEFAULT_TRANSPORT
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT


class TunnelingSettingsScheme(BaseModel):
    current: str = DEFAULT_TUNNELING_SERVICE
    use: bool = True
    public_url: str = ''


class GraphicsSettingsScheme(BaseModel):
    resolution: tuple = DEFAULT_RESOLUTION
    theme: str = Field(DEFAULT_THEME)


class DefaultSettingsScheme(BaseModel):
    hook: HookSettingsScheme = HookSettingsScheme()
    payload: PayloadSettingsScheme = PayloadSettingsScheme()
    transport: TransportSettingsScheme = TransportSettingsScheme()
    tunneling: TunnelingSettingsScheme = TunnelingSettingsScheme()
    graphics: GraphicsSettingsScheme = GraphicsSettingsScheme()
