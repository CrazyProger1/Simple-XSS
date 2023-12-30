from src.utils import arguments, di
from .schemes import DefaultArgumentsScheme

arguments_schema = di.Dependency(DefaultArgumentsScheme)
current_arguments = di.Dependency(DefaultArgumentsScheme)
arguments_parser = di.Dependency(arguments.SchemedArgumentParser)
