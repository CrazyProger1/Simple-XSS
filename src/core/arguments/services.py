from pydantic import BaseModel
from typeguard import typechecked

from src.utils import di, argutil
from .dependencies import ArgumentsDependencyContainer
from .events import ArgumentsEventChannel


@di.inject
@typechecked
def parse_arguments(
        parser: argutil.SchemedArgumentParser = ArgumentsDependencyContainer.argument_parser,
        args: list[str] | None = None,

) -> BaseModel:
    parsed_arguments = parser.parse_typed_args(
        args=args
    )
    di.bind(ArgumentsDependencyContainer.current_arguments, parsed_arguments)
    ArgumentsEventChannel.arguments_parsed()
    return parsed_arguments
