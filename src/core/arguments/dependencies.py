from pydantic import BaseModel

from src.utils import di, argutil

from .schemes import DefaultArgumentsScheme


class ArgumentsDependencyContainer(di.DeclarativeContainer):
    current_arguments: BaseModel
    argument_parser: argutil.SchemedArgumentParser

    @classmethod
    def configure(cls):
        di.bind(cls.argument_parser, argutil.SchemedArgumentParser(scheme=DefaultArgumentsScheme))
