import asyncio

from simplexss.core.logging import logger
from simplexss.core.types import BaseCore
from simplexss.core.utils import (
    load_hooks,
    load_payloads,
    load_plugins
)
from simplexss.core.channels import CoreChannel
from simplexss.core.containers import CoreContainer
from simplexss.core.arguments import parse_arguments

from simplexss.core.settings import (
    load_settings,
    save_settings
)
from simplexss.utils.di import (
    inject,
    setup
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
    CoreChannel.plugins_loaded.publish()

    arguments = parse_arguments()
    CoreContainer.arguments.bind(arguments)
    CoreChannel.arguments_loaded.publish()
    logger.info(f'Arguments loaded: {arguments}')

    settings = load_settings()
    CoreContainer.settings.bind(settings)
    CoreChannel.settings_loaded.publish()
    logger.info(f'Settings loaded: {settings}')

    load_hooks()
    logger.info('Hooks loaded')
    CoreChannel.hooks_loaded.publish()

    load_payloads()
    logger.info('Payloads loaded')
    CoreChannel.payloads_loaded.publish()

    await run_core()

    save_settings()

    logger.info('Application terminated')


if __name__ == '__main__':
    asyncio.run(main())
