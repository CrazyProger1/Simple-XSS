from pydantic import BaseModel
from src.utils import arguments, di
from .dependencies import arguments_parser, current_arguments


@di.injector.inject
def parse_arguments(
        parser: arguments.SchemedArgumentParser = arguments_parser,
        args: list[str] = None,

) -> BaseModel:
    parsed_arguments = parser.parse_typed_args(
        args=args
    )
    di.injector.bind(current_arguments, parsed_arguments)
    return parsed_arguments
