import asyncio
import argparse

from app.cli import CLI
from app.gui import GUI
from settings import (
    VERSION,
    APP
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
    return parser.parse_args()


async def main():
    args = parse_args()
    if args.graphic:
        gui = GUI(args)
        await gui.run()

    else:
        cli = CLI(args)
        await cli.run()


if __name__ == '__main__':
    asyncio.run(main())
