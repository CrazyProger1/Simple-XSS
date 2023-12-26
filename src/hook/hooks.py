from abc import ABC


class BaseHook(ABC):
    AUTHOR: str
    DESCRIPTION: str = None
    NAME: str
    VERSION: str
    TRANSPORT: str
