import asyncio

from i18n import (
    set_language
)

import simplexss.api
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

    await CoreChannel.plugins_loaded.publish_async()

    arguments = parse_arguments()
    CoreContainer.arguments.bind(arguments)
    await CoreChannel.arguments_loaded.publish_async()

    set_language(arguments.language)

    settings = load_settings()
    CoreContainer.settings.bind(settings)
    await CoreChannel.settings_loaded.publish_async()

    load_hooks()

    await CoreChannel.hooks_loaded.publish_async()

    load_payloads()

    await CoreChannel.payloads_loaded.publish_async()

    await run_core()

    save_settings()

    logger.info('Application terminated')


if __name__ == '__main__':
    asyncio.run(main())
