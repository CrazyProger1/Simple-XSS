from pydantic import BaseModel

from src.utils import di, argutil

current_arguments_dependency = di.Dependency(BaseModel)
argument_parser_dependency = di.Dependency(argutil.SchemedArgumentParser)
