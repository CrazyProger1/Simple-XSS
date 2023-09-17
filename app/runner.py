from app.settings import Settings
from app.session import ClientSession
from app.environment import Environment
from app.tunneling import HTTPTunnelingAppWrapper
from app.server import LocalWebsocketServer, DefaultWebsocketServer
from app.hook import Hook, DefaultHook
from app.payload import DefaultPayload
from app.utils import observer, url
from app.exceptions import HTTPTunnelError
from app.io import IOManager
from app.utils.settings import Format
from config import SETTINGS_FILE


class Runner:
    """Encapsulates & controls the functional part of the application"""

    @property
    def hook(self) -> Hook:
        raise NotImplementedError

    @property
    def server(self) -> LocalWebsocketServer:
        raise NotImplementedError

    @property
    def settings(self) -> Settings:
        raise NotImplementedError

    @property
    def environment(self):
        raise NotImplementedError

    async def run(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError


class DefaultRunner(Runner):
    tunneling_app_launched = observer.AsyncEvent()
    tunneling_app_launching_error = observer.AsyncEvent()  # event because it is non-critical
    tunneling_app_stopped = observer.AsyncEvent()

    ask_public_url = observer.Event()  # event because it is non-critical

    server_launched = observer.AsyncEvent()
    server_stopped = observer.AsyncEvent()

    hook_loaded = observer.AsyncEvent()
    payload_uploaded = observer.AsyncEvent()

    client_connected = observer.AsyncEvent()
    client_disconnected = observer.AsyncEvent()

    def __init__(self, settings: Settings, io: IOManager):
        import payload
        payload.io = io

        self._io = io
        self._settings = settings
        self._env = Environment(self._settings.public_url)
        self._server = DefaultWebsocketServer(settings.host, settings.port)
        self._tunneling_app: HTTPTunnelingAppWrapper | None = None
        self._hook = None
        self._stop = False

        LocalWebsocketServer.client_connected.add_listener(self._on_client_connected)
        LocalWebsocketServer.client_disconnected.add_listener(self._on_client_disconnected)
        LocalWebsocketServer.stopped.add_listener(self._on_server_stopped)
        LocalWebsocketServer.launched.add_listener(self._on_server_launched)

        HTTPTunnelingAppWrapper.stopped.add_listener(self._on_tunneling_app_stopped)

    async def _on_client_connected(self, session: ClientSession):
        await self.client_connected(session=session)
        self._io.print_pos(f'Client hooked: {session.connection.origin}')
        payload = DefaultPayload.load(self._settings.payload_path, environment=self._env)
        session.environment = self._env
        session.payload = payload
        session.hook = self._hook
        await self._server.send(session=session, message=str(payload))
        await self.payload_uploaded(session=session)
        self._io.print_debug(f'Payload uploaded: {session.connection.origin}')

    async def _on_client_disconnected(self, session: ClientSession):
        await self.client_disconnected(session=session)
        self._io.print_debug(f'Client escaped: {session.connection.origin}')

    async def _run_tunneling_app(self):
        try:
            self._tunneling_app = HTTPTunnelingAppWrapper.get_wrapper(
                self._settings.tunneling_app
            )(
                self._settings.host,
                self._settings.port
            )

            await self._tunneling_app.run()

            self._settings.public_url = url.convert_url(self._tunneling_app.public_url)

            await self.tunneling_app_launched(public_url=self._settings.public_url)
            self._io.print_debug(
                f'Tunneling app is up: {self._settings.public_url} -> {self._settings.host}:{self._settings.port}'
            )
        except (HTTPTunnelError, TypeError) as e:
            await self.tunneling_app_launching_error(error=e)
            self._io.print_debug(f'Failed to open tunnel')

    async def _on_server_launched(self, host, port):
        await self.server_launched(host=host, port=port)
        self._io.print_debug(f'Local server is listening: {self._settings.host}:{self._settings.port}')

    async def _on_server_stopped(self, host, port):
        await self.server_stopped(host=host, port=port)
        self._io.print_debug(f'Local server stopped')

    async def _on_tunneling_app_stopped(self, public_url: str):
        self._io.print_debug(f'Tunneling app stopped')

    async def _run_server(self):
        await self._server.run()

    async def _load_hook(self):
        self._hook = DefaultHook.load(self._settings.hook_path, environment=self._env)
        await self.hook_loaded(hook=self._hook)
        self._io.print_pos('Hook:', self._hook)

    @property
    def hook(self) -> Hook:
        return self._hook

    @property
    def server(self) -> LocalWebsocketServer:
        return self._server

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def environment(self) -> Environment:
        return self._env

    async def run(self):
        if self._settings.use_tunneling_app:
            await self._run_tunneling_app()
        else:
            self.ask_public_url()

        self._env.public_url = url.convert_url(self._settings.public_url)

        self._settings.save(Format.TOML, SETTINGS_FILE)

        await self._load_hook()
        await self._run_server()

    async def stop(self):
        await self.server.stop()
        if self._tunneling_app:
            await self._tunneling_app.stop()
