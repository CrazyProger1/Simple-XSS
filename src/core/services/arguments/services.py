from pydantic import BaseModel
from src.utils import argutil


def parse_arguments(
        parser: argutil.SchemedArgumentParser,
        args: list[str] = None,

) -> BaseModel:
    parsed_arguments = parser.parse_typed_args(
        args=args
    )
    return parsed_arguments
