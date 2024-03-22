from dataclasses import dataclass

from simplexss.core.types import (
    BaseHook,
    BasePayload
)


@dataclass
class Session:
    host: str
    port: int
    hook: BaseHook
    payload: BasePayload
