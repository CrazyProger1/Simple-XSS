from abc import ABC
from typing import Container


class BasePayload(ABC):
    AUTHOR: str
    DESCRIPTION: str = None
    NAME: str
    VERSION: str
    TRANSPORT: Container[str]
