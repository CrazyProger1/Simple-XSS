import asyncio
import argparse

from loguru import logger

from config import (
    APP,
    LOGGING_LEVEL,
    LOGGING_VERBOSITY,
    LOG_FILE
)


def setup_logging():
    """Sets up logging"""

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

    parser = argparse.ArgumentParser(
        APP,
        description=f'{APP} is a multiplatform cross-site scripting (XSS) '
                    'vulnerability exploitation tool for pentesting.'
    )
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
    parser.add_argument(
        '-c',
        '--create-hook',
        action='store_true',
        help='create hook'
    )
    parser.add_argument(
        '-p',
        '--create-payload',
        action='store_true',
        help='create payload'
    )
    return parser.parse_args()


@logger.catch()
async def main():
    setup_logging()
    args = parse_args()

    if args.create_hook:
        import scripts.create_hook
        return
    elif args.create_payload:
        import scripts.create_payload
        return

    elif args.graphic or args.browser:
        from app.gui import GUI
        app = GUI(args)

    else:
        from app.cli import CLI
        app = CLI(args)

    await app.run()


if __name__ == '__main__':
    asyncio.run(main())
