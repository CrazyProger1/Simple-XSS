import asyncio

from pydantic import BaseModel

from simplexss.core.config import PLUGINS_DIRECTORY, PLUGIN_FILE
from simplexss.core.logging import logger
from simplexss.core.types import BaseCore
from simplexss.core.containers import CoreContainer
from simplexss.core.channels import CoreChannel
from simplexss.utils.args import BaseSchemedArgumentParser
from simplexss.utils.settings import BaseLoader
from simplexss.utils.packages import (
    BasePackage,
    BasePackageManager
)
from simplexss.utils.di import (
    inject,
    setup
)


@inject
def load_settings(
        loader: BaseLoader = CoreContainer.settings_loader,
        arguments=CoreContainer.arguments,
        schema: type[BaseModel] = CoreContainer.settings_schema
):
    return loader.load(arguments.settings_file, schema)


@inject
def save_settings(

        loader: BaseLoader = CoreContainer.settings_loader,
        arguments=CoreContainer.arguments,
        settings=CoreContainer.settings,
):
    loader.save(arguments.settings_file, settings)


@inject
def parse_arguments(parser: BaseSchemedArgumentParser = CoreContainer.arguments_parser, ):
    return parser.parse_schemed_args()


@inject
def load_plugins(
        cls: BasePackage = CoreContainer.plugin_class,
        manager: BasePackageManager = CoreContainer.plugin_manager
):
    manager.load_packages(
        PLUGINS_DIRECTORY,
        class_name=cls.__name__,
        base_class=cls,
        file=PLUGIN_FILE,
    )


@inject
async def run_core(core: BaseCore = CoreContainer.core):
    await core.run()


async def main():
    logger.info('Application started')

    setup()
    logger.info(f'DI containers configured')

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
