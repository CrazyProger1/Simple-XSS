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

        self._runner = DefaultRunner(
            options=self._options,
            io=CLIIOManager()
        )

    async def _on_public_url_unspecified_error(self):
        self._options.public_url = url.convert_url(cli.ask_validated(
            f'Public url ({self._options.public_url}):',
            validator=validate_url,
            default=self._options.public_url
        ))

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
