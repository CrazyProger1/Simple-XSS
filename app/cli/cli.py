import payload
from app.app import App
from app.exceptions import OptionsLoadingError
from app.hook import DefaultHook
from app.options import Options
from app.payload import DefaultPayload
from app.utils import cli, url
from app.validators import validate_url
from app.runner import DefaultRunner
from .io import CLIIOManager
from .menu import Menu


class CLI(App):
    """Command Line Interface"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        payload.io = CLIIOManager()

        try:
            self._options = Options.load()
        except OptionsLoadingError:
            self._options = Options()

        self._runner = DefaultRunner(
            options=self._options,
            io=payload.io
        )
        self._menu = Menu(
            options=self._options,
            io=payload.io
        )

        self._runner.ask_public_url.add_listener(self._menu.ask_public_url)

    async def run(self):
        self._menu.run()

        await self._runner.run()
