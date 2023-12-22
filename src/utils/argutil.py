import argparse
import inspect
from typing import Container
from enum import Enum

import pydantic


class ArgumentParser(argparse.ArgumentParser):
    def __init__(
            self,
            *args,
            schema: type[pydantic.BaseModel] | None = None,
            ignore: Container[str] | None = None,
            positional: Container[str] | None = None,
            short_aliases: dict[str, str] = None or {},
            **kwargs
    ):

        super(ArgumentParser, self).__init__(*args, **kwargs)
        self._schema = schema
        self._ignore = ignore or set()
        self._positional = positional or set()
        self._short_aliases = short_aliases

        if schema:
            self._add_arguments()

    def _get_field_converter(self, field_info: pydantic.fields.FieldInfo):
        field_type = field_info.annotation

        if inspect.isclass(field_type) and issubclass(field_type, Enum):
            return field_type

        def argument(value: str):  # validator (such named to display the error correctly)
            if field_info.metadata:
                for validator in field_info.metadata:
                    try:
                        validator.func(value)
                    except (ValueError, AssertionError):
                        raise ValueError()

            return value

        return argument

    def _add_arguments(self):
        for field_name, field_info in self._schema.model_fields.items():
            field_type = field_info.annotation

            if field_name in self._ignore:
                continue

            args = []
            kwargs = {
                'default': field_info.default,
                'help': field_info.description,
                'type': self._get_field_converter(field_info),
            }

            if field_name not in self._positional:
                short_alias = self._short_aliases.get(field_name, field_name)

                args.extend((f'-{short_alias[0]}', f'--{field_name}',))
            else:
                args.append(field_name)

                if not field_info.is_required():
                    kwargs.update({'nargs': '?'})

            if inspect.isclass(field_type) and issubclass(field_type, Enum):
                kwargs.update({
                    'choices': list(map(lambda c: c.value, field_type))
                })

            self.add_argument(
                *args,
                **kwargs,
            )

    def parse_typed_args(self, args=None, namespace=None) -> pydantic.BaseModel:
        namespace = self.parse_args(args=args, namespace=namespace)
        return self._schema.model_validate(namespace.__dict__)
