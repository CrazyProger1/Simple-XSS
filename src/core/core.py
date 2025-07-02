import logging

from src.core.events import CoreEventChannel

logger = logging.getLogger("simplexss")


async def core():
    await CoreEventChannel.application_launched.publish_async()

    logger.info("Simple-XSS launched")

    await CoreEventChannel.plugins_loaded.publish_async()

    logger.info("Plugins loaded")

    await CoreEventChannel.arguments_parsed.publish_async()

    logger.info("Arguments parsed")

    await CoreEventChannel.settings_loaded.publish_async()

    logger.info("Settings loaded")

    await CoreEventChannel.application_terminated.publish_async()

    logger.info("Simple-XSS terminated")
