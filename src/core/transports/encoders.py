from abc import ABC, abstractmethod
from .schemes import BaseEventScheme


class BaseEncoder(ABC):
    @classmethod
    @abstractmethod
    def encode(cls, event: BaseEventScheme) -> str: ...

    @classmethod
    @abstractmethod
    def decode(cls, raw: str, scheme: type[BaseEventScheme]) -> BaseEventScheme: ...


class JSONEncoder(BaseEncoder):
    @classmethod
    def encode(cls, event: BaseEventScheme) -> str:
        raw = event.model_dump_json()
        return raw

    @classmethod
    def decode(cls, raw: str, scheme: type[BaseEventScheme]) -> BaseEventScheme:
        return scheme.model_validate_json(raw)
