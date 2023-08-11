from app.app import App
from app.environment import Environment
from app.exceptions import HTTPTunnelError, OptionsLoadingError
from app.hook import DefaultHook
from app.options import Options
from app.payload import DefaultPayload
from app.server import DefaultWebsocketServer, LocalWebsocketServer
from app.session import ClientSession
from app.tunneling import HTTPTunnelingAppWrapper
from app.utils import cli, url
from app.validators import validate_url
from settings import OPTIONS_FILE


class CLI(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._options = Options.load(OPTIONS_FILE)
        except OptionsLoadingError:
            self._options = Options()

        self._server = DefaultWebsocketServer(self._options.host, self._options.port)
        self._hook = None
        self._env = Environment()
        LocalWebsocketServer.client_connected.add_listener(self._on_client_connected)

    async def _on_client_connected(self, session: ClientSession):
        payload = DefaultPayload.load(self._options.payload_path, environment=self._env)
        session.environment = self._env
        session.payload = payload
        session.hook = self._hook
        await self._server.send(session=session, message=str(payload))

    async def _run_tunneling_app(self, app: str):
        try:
            wrapper = HTTPTunnelingAppWrapper.get_wrapper(app)(self._options.host, self._options.port)
            await wrapper.run()
            self._public_url = wrapper.public_url
        except HTTPTunnelError:
            pass

    async def _run_server(self):
        await self._server.run()

    async def _load_hook(self, hook_path: str):
        self._hook = DefaultHook.load(hook_path, environment=self._env)
        cli.print_pos('Hook:', self._hook)

    async def run(self):

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

        use_tunneling_app = cli.ask_bool('Use tunneling app (Y/N):', default=False)
        if use_tunneling_app:
            app = cli.ask_option(
                f'Choose app ({self._options.tunneling_app}):',
                options=[wrapper.app for wrapper in HTTPTunnelingAppWrapper.__subclasses__()],
                default=self._options.tunneling_app
            )
            await self._run_tunneling_app(app)

        if not self._options.public_url:
            self._options.public_url = cli.ask_validated(
                f'Public url ({self._options.public_url}):',
                validator=validate_url,
                default=self._options.public_url
            )

        self._env.public_url = url.convert_url(self._options.public_url)

        self._options.save()
        await self._load_hook(hook_path=self._options.hook_path)
        await self._run_server()
