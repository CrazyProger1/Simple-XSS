import flet as ft
from pydantic import BaseModel

from src.core.config import (
    DEFAULT_RESOLUTION
)


class HookSettingsScheme(BaseModel):
    current: str = None
    directory: str = './resources/hooks'


class PayloadSettingsScheme(BaseModel):
    current: str = None
    directory: str = './resources/payloads'


class TransportSettingsScheme(BaseModel):
    current: str = 'http'
    directory: str = './resources/services/transport'
    host: str = 'localhost'
    port: int = 4444


class TunnellingSettingsScheme(BaseModel):
    current: str = 'ngrok'
    directory: str = './resources/services/tunnelling'
    use: bool = True
    public_url: str = ''


class GraphicsSettingsScheme(BaseModel):
    resolution: tuple = DEFAULT_RESOLUTION
    theme: ft.ThemeMode = ft.ThemeMode.DARK


class DefaultSettingsScheme(BaseModel):
    hook: HookSettingsScheme = HookSettingsScheme()
    payload: PayloadSettingsScheme = PayloadSettingsScheme()
    transport: TransportSettingsScheme = TransportSettingsScheme()
    tunnelling: TunnellingSettingsScheme = TunnellingSettingsScheme()
    graphics: GraphicsSettingsScheme = GraphicsSettingsScheme()
