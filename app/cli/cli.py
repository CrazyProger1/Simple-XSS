from app.app import App
from app.hook import DefaultHook
from app.payload import DefaultPayload
from app.utils import cli, url
from app.tunneling import HTTPTunnelingAppWrapper
from app.server import DefaultWebsocketServer, LocalWebsocketServer
from app.exceptions import HTTPTunnelError
from app.validators import validate_url
from app.environment import Environment
from app.session import ClientSession


class CLI(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._public_url = None
        self._server = DefaultWebsocketServer('localhost', 4444)
        self._hook = None
        self._payload_path = None
        self._env = Environment()
        LocalWebsocketServer.client_connected.add_listener(self._on_client_connected)

    async def _on_client_connected(self, session: ClientSession):
        payload = DefaultPayload.load(self._payload_path, environment=self._env)
        session.environment = self._env
        session.payload = payload
        session.hook = self._hook
        await self._server.send(session=session, message=str(payload))

    async def _run_tunneling_app(self, app: str):
        try:
            wrapper = HTTPTunnelingAppWrapper.get_wrapper(app)('localhost', 4444)
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
        hook_path = cli.ask_validated('Hook path:', validator=DefaultHook.is_valid)
        self._payload_path = cli.ask_validated('Payload path:', validator=DefaultPayload.is_valid)

        use_tunneling_app = cli.ask_bool('Use tunneling app (Y/N):')
        if use_tunneling_app:
            app = cli.ask_option(
                'Choose app:',
                options=[wrapper.app for wrapper in HTTPTunnelingAppWrapper.__subclasses__()]
            )
            await self._run_tunneling_app(app)

        if not self._public_url:
            self._public_url = cli.ask_validated('Public url:', validate_url)

        self._env.public_url = url.convert_url(self._public_url)

        await self._load_hook(hook_path=hook_path)
        await self._run_server()
