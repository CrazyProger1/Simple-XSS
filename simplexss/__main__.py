import asyncio

from pydantic import BaseModel

from simplexss.core.logging import logger
from simplexss.core.types import BaseCore
from simplexss.core.containers import CoreContainer
from simplexss.core.channels import CoreChannel
from simplexss.utils.args import BaseSchemedArgumentParser
from simplexss.utils.settings import BaseLoader
from simplexss.utils.di import (
    inject,
    setup
)


@inject
def load_settings(
        arguments=CoreContainer.arguments,
        loader: BaseLoader = CoreContainer.settings_loader,
        schema: type[BaseModel] = CoreContainer.settings_schema
):
    return loader.load(arguments.settings_file, schema)


@inject
def save_settings(
        arguments=CoreContainer.arguments,
        loader: BaseLoader = CoreContainer.settings_loader,
        settings=CoreContainer.settings,
):
    loader.save(arguments.settings_file, settings)


@inject
def parse_arguments(parser: BaseSchemedArgumentParser = CoreContainer.arguments_parser, ):
    return parser.parse_schemed_args()


@inject
def load_plugins():
    pass


@inject
async def run_core(core: BaseCore = CoreContainer.core):
    await core.run()


async def main():
    logger.info('Application started')

    setup()

    load_plugins()
    logger.info(f'Plugins loaded')

    arguments = parse_arguments()
    CoreContainer.arguments.bind(arguments)
    await CoreChannel.arguments_loaded.publish_async()
    logger.info(f'Arguments loaded: {arguments}')

    settings = load_settings()
    CoreContainer.settings.bind(settings)
    await CoreChannel.settings_loaded.publish_async()
    logger.info(f'Settings loaded: {settings}')

    await run_core()

    save_settings()

    logger.info('Application terminated')


if __name__ == '__main__':
    asyncio.run(main())
