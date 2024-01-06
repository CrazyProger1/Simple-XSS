from pydantic import BaseModel

from src.utils import di, argutil

current_arguments = di.Dependency(BaseModel)
argument_parser = di.Dependency(argutil.SchemedArgumentParser)
