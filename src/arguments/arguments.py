from pydantic import BaseModel
from src.utils import arguments


def parse_arguments(
        parser: arguments.SchemedArgumentParser,
        args: list[str] = None,

) -> BaseModel:
    return parser.parse_typed_args(
        args=args
    )
