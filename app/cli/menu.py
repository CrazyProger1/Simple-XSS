import colorama
from tabulate import tabulate
from app.hook import DefaultHook
from app.io import IOManager
from app.options import Options
from app.payload import DefaultPayload
from app.utils import cli, url
from app.validators import validate_url
from settings import APP, VERSION


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

    def ask_use_tunneling_app(self):
        self._options.use_tunneling_app = cli.ask_bool('Use tunneling app (Y/N):', default=False)

    def ask_about_tunneling_app(self):
        self.ask_use_tunneling_app()

        if self._options.use_tunneling_app:
            self.ask_public_url()

    def show_options(self):
        print(tabulate(self._options.__dict__.items(), headers=['NAME', 'VALUE'], tablefmt='grid'))

    def set(self):
        while True:
            print()
            self.show_options()

            options = {
                'public url': self.ask_public_url,
                'payload path': self.ask_payload_path,
                'hook path': self.ask_hook_path,
                'tunneling app': self.ask_about_tunneling_app,
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
                    'set',
                    'run',
                    'exit',
                )
            )

            match option:
                case 'set':
                    self.set()
                case 'run':
                    break
                case 'exit':
                    exit()
