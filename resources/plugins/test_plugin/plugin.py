import argparse
from typing import Sequence

import pydantic

from src.arguments.dependencies import arguments_parser, arguments_schema
from src.plugins import BasePlugin
from src.utils import arguments, di


class MyParser(arguments.SchemedArgumentParser):
    def parse_typed_args(
            self,
            args: Sequence[str] = None,
            namespace: argparse.Namespace = None
    ) -> pydantic.BaseModel:
        print('PARSING ARGS WITH PLUGIN!!!!!!')
        return super(MyParser, self).parse_typed_args()


class Plugin(BasePlugin):
    AUTHOR = 'crazyproger1'
    NAME = 'Test plugin'
    VERSION = '0.1'

    def __init__(self):
        di.injector.bind(
            arguments_parser,
            MyParser(
                schema=di.injector.get_dependency(arguments_schema)
            )
        )
