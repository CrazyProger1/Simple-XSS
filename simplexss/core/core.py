import logging

from simplexss.core.events import CoreEventChannel

logger = logging.getLogger("simplexss")


async def core():
    logger.info("Launching Simple-XSS...")

    await CoreEventChannel.application_launched.publish_async()

    await CoreEventChannel.application_terminated.publish_async()

    logger.info("Simple-XSS terminated")
