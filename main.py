import asyncio
import argparse

from loguru import logger
from app.cli import CLI
from app.gui import GUI
from settings import (
    VERSION,
    APP,
    LOGGING_LEVEL,
    LOGGING_VERBOSITY,
    LOG_FILE
)


def setup_logging():
    if not LOGGING_VERBOSITY:
        logger.remove()

    logger.add(
        LOG_FILE,
        level=LOGGING_LEVEL,
        rotation='100 KB',
        compression='zip'
    )


def parse_args() -> argparse.Namespace:
    """Parses console arguments"""

    parser = argparse.ArgumentParser(APP, description='XSS vulnerability payload builder')
    parser.add_argument(
        '-g',
        '--graphic',
        action='store_true',
        help='graphic interface'
    )
    parser.add_argument(
        '-b',
        '--browser',
        action='store_true',
        help='browser interface'
    )
    return parser.parse_args()


async def main():
    setup_logging()
    args = parse_args()
    if args.graphic or args.browser:
        gui = GUI(args)
        await gui.run()

    else:
        cli = CLI(args)
        await cli.run()


if __name__ == '__main__':
    asyncio.run(main())
