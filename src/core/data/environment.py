from dataclasses import dataclass
from src.core.settings import DefaultSettingsScheme
from src.core.hooks import BaseHook
from src.core.payloads import BasePayload


@dataclass
class Environment:
    settings: DefaultSettingsScheme
    hook: BaseHook = None
    payload: BasePayload = None
