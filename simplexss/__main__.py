import asyncio
import logging

from simplexss.core.config import LOGGING_CONFIG_FILE
from simplexss.core.logging import configure_logging

logger = logging.getLogger("simplexss")


async def main():
    configure_logging(LOGGING_CONFIG_FILE)

    logger.info("Launching Simple-XSS...")

    logger.info("Simple-XSS terminated")


if __name__ == "__main__":
    asyncio.run(main())
