from dataclasses import dataclass
from ..types import (
    BaseSession
)


@dataclass(frozen=True)
class HTTPSession(BaseSession):
    pass
