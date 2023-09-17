from app.app import App
from app.runner import DefaultRunner
from .io import CLIIOManager
from .menu import Menu


class CLI(App):
    """Command Line Interface"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        io = CLIIOManager()

        self._runner = DefaultRunner(
            settings=self._settings,
            io=io
        )
        self._menu = Menu(
            options=self._settings,
            io=io
        )

        self._runner.ask_public_url.add_listener(self._menu.ask_public_url)

    async def run(self):
        self._menu.run()
        await self._runner.run()
