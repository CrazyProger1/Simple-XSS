import argparse
import inspect
from typing import Container, Sequence
from enum import Enum

import pydantic
from typeguard import typechecked
from loguru import logger


class SchemedArgumentParser(argparse.ArgumentParser):
    @typechecked
    def __init__(
            self,
            *,
            schema: type[pydantic.BaseModel] | None = None,
            ignore_fields: Container[str] | None = None,
            positional_arguments: Container[str] | None = None,
            short_aliases: dict[str, str] | None = None,
            **kwargs
    ):

        super(SchemedArgumentParser, self).__init__(**kwargs)
        self._schema = schema
        self._ignore_fields = ignore_fields or set()
        self._positional_arguments = positional_arguments or set()
        self._short_aliases = short_aliases or {}

        if schema:
            self._add_arguments_from_schema()

    @staticmethod
    def _is_enum_field(field_type: type):
        return inspect.isclass(field_type) and issubclass(field_type, Enum)

    @staticmethod
    def _convert_enum_value(value: str, enum: type[Enum]):
        if issubclass(enum, int):
            return enum(int(value))
        return enum(value)

    def _convert_value(
            self,
            value: str,
            field_info: pydantic.fields.FieldInfo
    ):
        field_type = field_info.annotation

        if self._is_enum_field(field_type):
            return self._convert_enum_value(value, enum=field_type)

        if field_info.metadata:
            for validator in field_info.metadata:
                try:
                    validator.func(value)
                except (ValueError, AssertionError):
                    raise ValueError()

        return value

    def _get_value_converter(self, field_info: pydantic.fields.FieldInfo):
        def argument(value: str):
            return self._convert_value(value, field_info)

        return argument

    def _add_field_argument(
            self,
            field_name: str,
            field_info: pydantic.fields.FieldInfo
    ):
        field_type: type = field_info.annotation

        args = []
        kwargs = {
            'default': field_info.default,
            'help': field_info.description,
            'type': self._get_value_converter(field_info),
        }

        if field_name not in self._positional_arguments:
            short_alias = self._short_aliases.get(field_name, field_name)
            args.extend((f'-{short_alias[0]}', f'--{field_name}',))
        else:
            args.append(field_name)

            if not field_info.is_required():
                kwargs.update({'nargs': '?'})

        if self._is_enum_field(field_type):
            kwargs.update({
                'choices': list(map(lambda c: c.value, field_type))
            })

        self.add_argument(
            *args,
            **kwargs,
        )

    def _add_arguments_from_schema(self):
        fields = self._schema.model_fields

        for field_name, field_info in fields.items():
            if field_name not in self._ignore_fields:
                self._add_field_argument(
                    field_name=field_name,
                    field_info=field_info
                )

    def parse_typed_args(
            self,
            args: Sequence[str] = None,
            namespace: argparse.Namespace = None
    ) -> pydantic.BaseModel:
        logger.info('Parsing arguments')
        namespace = self.parse_args(args=args, namespace=namespace)
        logger.info(f'Args: {namespace}')
        return self._schema.model_validate(namespace.__dict__)
