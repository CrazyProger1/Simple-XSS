from pydantic import BaseModel

from src.utils import argutil, di
from .dependencies import argument_parser_dependency, current_arguments_dependency
from .events import arguments_parsed


@di.injector.inject
def parse_arguments(
        parser: argutil.SchemedArgumentParser = argument_parser_dependency,
        args: list[str] = None,

) -> BaseModel:
    parsed_arguments = parser.parse_typed_args(
        args=args
    )
    di.injector.bind(current_arguments_dependency, parsed_arguments)
    arguments_parsed()
    return parsed_arguments
