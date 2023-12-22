from pydantic import BaseModel


class HookSettingsSchema(BaseModel):
    current: str
    directory: str = './resources/payloads'


class PayloadSettingsSchema(BaseModel):
    current: str
    directory: str = './resources/payloads'


class TransportSettingsSchema(BaseModel):
    current: str = 'http'
    directory: str = './resources/services/transport'
    host: str = 'localhost'
    port: int = 4444


class TunnellingSettingsSchema(BaseModel):
    current: str = 'ngrok'
    directory: str = './resources/services/tunnelling'
    use: bool = True
    public_url: str = ''


class SettingsSchema(BaseModel):
    hook: HookSettingsSchema
    payload: PayloadSettingsSchema
    transport: TransportSettingsSchema
    tunnelling: TunnellingSettingsSchema
