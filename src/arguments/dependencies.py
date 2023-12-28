from src.utils import arguments, di
from .schemas import DefaultArgumentsSchema

arguments_schema = di.Dependency(DefaultArgumentsSchema)
current_arguments = di.Dependency(DefaultArgumentsSchema)
arguments_parser = di.Dependency(arguments.SchemedArgumentParser)
