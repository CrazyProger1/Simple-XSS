import os
from abc import ABC, abstractmethod
from typing import get_type_hints
from enum import Enum
from functools import cache

import toml
from pydantic import BaseModel

from .exceptions import (
    SettingsDecodeError,
    SettingsEncodeError,
    SettingsSchemaError
)


class Format(Enum):
    TOML = 1


class SettingsSchema(BaseModel):
    @classmethod
    def load(cls, fmt: Format, file: str) -> 'SettingsSchema':
        loader = create_loader(fmt, cls)
        return loader.load(file)

    def save(self, fmt: Format, file: str) -> None:
        loader = create_loader(fmt, self.__class__)
        return loader.save(file, self)


class SettingsLoader(ABC):

    @abstractmethod
    def load(self, file: str) -> 'SettingsSchema': ...

    @abstractmethod
    def save(self, file: str, obj: SettingsSchema) -> None: ...


class TOMLSettingsLoader(SettingsLoader):
    def __init__(self, schema: type[SettingsSchema]):
        self.__schema = schema

    def __validate_curr_values(self, obj: SettingsSchema):
        annotations = get_type_hints(obj.__class__)
        for field, value in self.__dict__.items():
            if field == f'_{self.__class__.__name__}__schema':
                continue
            typehint = annotations.get(field)
            if not isinstance(value, typehint):
                raise SettingsEncodeError(f'Field {field} has wrong type value, it should be {typehint.__name__}')

    def __validate_field_types(self):
        annotations = get_type_hints(self.__schema)
        dumpable_types = set(toml.TomlEncoder().dump_funcs.keys())
        dumpable_types.add(dict)

        for field, typehint in annotations.items():
            if typehint not in dumpable_types and not issubclass(typehint, SettingsSchema):
                raise SettingsSchemaError(f'Field {field} has undumpable type')

    def load(self, file: str) -> 'SettingsSchema':
        self.__validate_field_types()

        if not os.path.isfile(file):
            raise FileNotFoundError(f'File {file} not found')
        try:
            data = toml.load(file)
        except toml.TomlDecodeError:
            raise SettingsDecodeError(f'File {file} has incorrect format, it should be toml')

        return self.__schema.model_validate(data)

    def save(self, file: str, obj: SettingsSchema) -> None:
        if not isinstance(obj, SettingsSchema):
            raise TypeError('obj must be instance of SettingsSchema')

        self.__validate_curr_values(obj)

        try:
            data = obj.model_dump()
        except TypeError:
            raise SettingsEncodeError('Encode error')

        with open(file, 'w', encoding='utf-8') as f:
            toml.dump(data, f)


@cache
def create_loader(fmt: Format, schema: type[SettingsSchema]) -> SettingsLoader:
    match fmt:
        case Format.TOML:
            return TOMLSettingsLoader(schema=schema)
