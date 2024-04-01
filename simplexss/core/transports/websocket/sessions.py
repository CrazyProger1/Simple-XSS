from dataclasses import dataclass
from ..types import (
    BaseSession
)


@dataclass(frozen=True)
class WebsocketSession(BaseSession):
    pass
