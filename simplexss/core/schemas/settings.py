from pydantic import BaseModel, Field

from simplexss.core.config import (
    DEFAULT_RESOLUTION,
    DEFAULT_THEME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_TRANSPORT,
    PAYLOADS_DIRECTORY,
    HOOKS_DIRECTORY,
    DEFAULT_TUNNELING_SERVICE
)


class HookSettingsSchema(BaseModel):
    current: str = None
    directory: str = HOOKS_DIRECTORY


class PayloadSettingsSchema(BaseModel):
    current: str = None
    directory: str = PAYLOADS_DIRECTORY


class TransportSettingsSchema(BaseModel):
    current: str = DEFAULT_TRANSPORT
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT


class TunnelingSettingsSchema(BaseModel):
    current: str = DEFAULT_TUNNELING_SERVICE
    use: bool = True
    public_url: str = ''


class GraphicsSettingsSchema(BaseModel):
    resolution: tuple = DEFAULT_RESOLUTION
    theme: str = Field(DEFAULT_THEME)


class SettingsSchema(BaseModel):
    hook: HookSettingsSchema = HookSettingsSchema()
    payload: PayloadSettingsSchema = PayloadSettingsSchema()
    transport: TransportSettingsSchema = TransportSettingsSchema()
    tunneling: TunnelingSettingsSchema = TunnelingSettingsSchema()
    graphics: GraphicsSettingsSchema = GraphicsSettingsSchema()