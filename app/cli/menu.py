import colorama
from tabulate import tabulate
from app.hook import DefaultHook
from app.io import IOManager
from app.options import Options
from app.payload import DefaultPayload
from app.utils import cli, url
from app.validators import (
    validate_url,
    validate_port,
    validate_host
)
from settings import (
    APP,
    VERSION,
    USE_TUNNELING_APP
)


class Menu:
    def __init__(self, options: Options, io: IOManager):
        self._options = options
        self._io = io

    def print_welcome(self):
        cli.print_colored(f'{APP} - V{VERSION}', color=colorama.Fore.BLUE + colorama.Style.BRIGHT)

    def ask_public_url(self):
        self._options.public_url = url.convert_url(cli.ask_validated(
            f'Public url ({self._options.public_url}):',
            validator=validate_url,
            default=self._options.public_url
        ))

    def ask_hook_path(self):
        self._options.hook_path = cli.ask_validated(
            f'Hook path ({self._options.hook_path}):',
            validator=DefaultHook.is_valid,
            default=self._options.hook_path
        )

    def ask_payload_path(self):
        self._options.payload_path = cli.ask_validated(
            f'Payload path ({self._options.payload_path}):',
            validator=DefaultPayload.is_valid,
            default=self._options.payload_path
        )

    def ask_port(self):
        self._options.port = int(cli.ask_validated(
            f'Port ({self._options.port}):',
            validator=validate_port,
            default=self._options.port
        ))

    def ask_host(self):
        self._options.host = cli.ask_validated(
            f'Host ({self._options.host}):',
            validator=validate_host,
            default=self._options.host
        )

    def ask_use_tunneling_app(self):
        self._options.use_tunneling_app = cli.ask_bool('Use tunneling app (Y/N):', default=USE_TUNNELING_APP)

    def ask_about_tunneling_app(self):
        self.ask_use_tunneling_app()

        if not self._options.use_tunneling_app:
            self.ask_public_url()

    def show_options(self):
        print()
        print(tabulate(self._options.__dict__.items(), headers=['NAME', 'VALUE'], tablefmt='grid'))

    def set(self):
        while True:
            self.show_options()

            print()

            options = {
                'public url': self.ask_public_url,
                'payload path': self.ask_payload_path,
                'hook path': self.ask_hook_path,
                'tunneling app': self.ask_about_tunneling_app,
                'host': self.ask_host,
                'port': self.ask_port,
                'back': None
            }

            option = cli.ask_option(
                'Choose option:',
                options=options.keys()
            )

            handler = options.get(option)

            if callable(handler):
                handler()

            if option == 'back':
                break

    def run(self):
        self.print_welcome()

        while True:
            print()
            option = cli.ask_option(
                'Choose option:',
                options=(
                    'show',
                    'set',
                    'run',
                    'exit',
                )
            )

            match option:
                case 'show':
                    self.show_options()
                case 'set':
                    self.set()
                case 'run':
                    break
                case 'exit':
                    exit()
