from pydantic import BaseModel

from src.utils import argutil, di
from src.core.dependencies import argument_parser, current_arguments


@di.injector.inject
def parse_arguments(
        parser: argutil.SchemedArgumentParser = argument_parser,
        args: list[str] = None,

) -> BaseModel:
    parsed_arguments = parser.parse_typed_args(
        args=args
    )
    di.injector.bind(current_arguments, parsed_arguments)
    return parsed_arguments
