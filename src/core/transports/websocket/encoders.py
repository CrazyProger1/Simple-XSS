from abc import ABC, abstractmethod

from pydantic import BaseModel, ValidationError
from typeguard import typechecked


class BaseEncoder(ABC):
    @classmethod
    @abstractmethod
    def encode(cls, data: BaseModel) -> str: ...

    @classmethod
    @abstractmethod
    def decode(cls, raw: str, scheme: type[BaseModel]) -> BaseModel: ...


class JSONEncoder(BaseEncoder):
    @classmethod
    @typechecked
    def encode(cls, data: BaseModel) -> str:
        return data.model_dump_json()

    @classmethod
    @typechecked
    def decode(cls, raw: str, scheme: type[BaseModel]) -> BaseModel:
        try:
            return scheme.model_validate_json(raw)
        except ValidationError:
            raise ValueError(f'Failed to decode: {raw}')
