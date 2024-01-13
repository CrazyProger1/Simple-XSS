from pydantic import BaseModel

from src.utils import di, argutil

from .schemes import DefaultArgumentsScheme


class ArgumentsDependencyContainer(di.DeclarativeContainer):
    current_arguments: BaseModel
    argument_scheme: DefaultArgumentsScheme = di.Dependency(DefaultArgumentsScheme)
    argument_parser: argutil.SchemedArgumentParser = di.Factory(
        argutil.SchemedArgumentParser,
        scheme=argument_scheme
    )
