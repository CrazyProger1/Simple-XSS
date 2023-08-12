import payload
from app.app import App
from app.exceptions import OptionsLoadingError
from app.hook import DefaultHook
from app.options import Options
from app.payload import DefaultPayload
from app.session import ClientSession
from app.utils import cli, url
from app.validators import validate_url
from app.runner import DefaultRunner
from .io import CLIIOManager


class CLI(App):
    """Command Line Interface"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        try:
            self._options = Options.load()
        except OptionsLoadingError:
            self._options = Options()

        self._runner = DefaultRunner(options=self._options)

        DefaultRunner.tunneling_app_launched.add_listener(self._on_tunneling_app_launched)
        DefaultRunner.tunneling_app_launching_error.add_listener(self._on_tunneling_app_error)
        DefaultRunner.public_url_unspecified_error.add_listener(self._on_public_url_unspecified_error)
        DefaultRunner.hook_loaded.add_listener(self._on_hook_loaded)
        DefaultRunner.payload_uploaded.add_listener(self._on_payload_uploaded)
        DefaultRunner.client_hooked.add_listener(self._on_client_hooked)
        DefaultRunner.server_launched.add_listener(self._on_server_launched)

    async def _on_client_hooked(self, session: ClientSession):
        cli.print_pos(f'Client hooked: {session.connection.origin}')

    async def _on_client_escaped(self, session: ClientSession):
        cli.print_pos(f'Client escaped: {session.connection.origin}')

    async def _on_payload_uploaded(self, session: ClientSession):
        cli.print_pos(f'Payload sent: {session.payload.metadata.name}')

    async def _on_hook_loaded(self, hook):
        cli.print_pos('Hook:', hook)

    async def _on_public_url_unspecified_error(self):
        self._options.public_url = url.convert_url(cli.ask_validated(
            f'Public url ({self._options.public_url}):',
            validator=validate_url,
            default=self._options.public_url
        ))

    async def _on_tunneling_app_launched(self, public_url: str):
        cli.print_pos(f'Tunneling app is up: {public_url} -> {self._options.host}:{self._options.port}')

    async def _on_tunneling_app_error(self, error: Exception):
        cli.print_neg(f'Failed to open tunnel')

    async def _on_server_launched(self, host, port):
        cli.print_pos(f'Local server app is listening: {self._options.host}:{self._options.port}')

    async def run(self):
        payload.io = CLIIOManager()
        self._options.hook_path = cli.ask_validated(
            f'Hook path ({self._options.hook_path}):',
            validator=DefaultHook.is_valid,
            default=self._options.hook_path
        )

        self._options.payload_path = cli.ask_validated(
            f'Payload path ({self._options.payload_path}):',
            validator=DefaultPayload.is_valid,
            default=self._options.payload_path
        )
        self._options.use_tunneling_app = cli.ask_bool('Use tunneling app (Y/N):', default=False)

        await self._runner.run()
