import argparse
from typing import Sequence

import pydantic
from loguru import logger
from pydantic import Field

from src.arguments.dependencies import arguments_parser
from src.arguments.schemes import DefaultArgumentsScheme
from src.plugins import BasePlugin
from src.utils import arguments, di


class MyArgSchema(DefaultArgumentsScheme):
    test: str = Field(default='abc', description='test arg')


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
        logger.info('I AM PLUGIN')
        di.injector.bind(
            arguments_parser,
            MyParser(
                schema=MyArgSchema
            )
        )
