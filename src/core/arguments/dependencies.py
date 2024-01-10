from pydantic import BaseModel

from src.utils import di, argutil

from .schemes import DefaultArgumentsScheme

current_arguments_dependency = di.Dependency(BaseModel, DefaultArgumentsScheme)
argument_parser_dependency = di.Dependency(argutil.SchemedArgumentParser)
