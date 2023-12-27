from pydantic import BaseModel


class HookSettingsSchema(BaseModel):
    current: str = None
    directory: str = './resources/payloads'


class PayloadSettingsSchema(BaseModel):
    current: str = None
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


class DefaultSettingsSchema(BaseModel):
    hook: HookSettingsSchema = HookSettingsSchema()
    payload: PayloadSettingsSchema = PayloadSettingsSchema()
    transport: TransportSettingsSchema = TransportSettingsSchema()
    tunnelling: TunnellingSettingsSchema = TunnellingSettingsSchema()
