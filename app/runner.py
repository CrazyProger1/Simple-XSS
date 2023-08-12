from app.options import Options
from app.session import ClientSession
from app.environment import Environment
from app.tunneling import HTTPTunnelingAppWrapper
from app.server import LocalWebsocketServer, DefaultWebsocketServer
from app.hook import Hook, DefaultHook
from app.payload import DefaultPayload
from app.utils import observer, url
from app.exceptions import HTTPTunnelError


class Runner:
    """Encapsulates & controls the functional part of the application"""

    @property
    def hook(self) -> Hook:
        raise NotImplementedError

    @property
    def server(self) -> LocalWebsocketServer:
        raise NotImplementedError

    @property
    def options(self) -> Options:
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
    public_url_unspecified_error = observer.AsyncEvent()  # event because it is non-critical
    server_launched = observer.AsyncEvent()
    hook_loaded = observer.AsyncEvent()
    client_hooked = observer.AsyncEvent()
    payload_uploaded = observer.AsyncEvent()
    client_escaped = observer.AsyncEvent()
    before_server_launching = observer.AsyncEvent()

    def __init__(self, options: Options):
        self._options = options
        self._env = Environment(self._options.public_url)
        self._server = DefaultWebsocketServer(options.host, options.port)
        self._tunneling_app: HTTPTunnelingAppWrapper | None = None
        self._hook = None
        self._stop = False
        LocalWebsocketServer.client_connected.add_listener(self._on_client_connected)
        LocalWebsocketServer.client_disconnected.add_listener(self.client_escaped)

    async def _on_client_connected(self, session: ClientSession):
        await self.client_hooked(session=session)
        payload = DefaultPayload.load(self._options.payload_path, environment=self._env)
        session.environment = self._env
        session.payload = payload
        session.hook = self._hook
        await self._server.send(session=session, message=str(payload))
        await self.payload_uploaded(session=session)

    async def _run_tunneling_app(self):
        try:
            self._tunneling_app = HTTPTunnelingAppWrapper.get_wrapper(
                self._options.tunneling_app
            )(
                self._options.host,
                self._options.port
            )

            await self._tunneling_app.run()

            self._options.public_url = url.convert_url(self._tunneling_app.public_url)

            await self.tunneling_app_launched(public_url=self._options.public_url)
        except (HTTPTunnelError, TypeError) as e:
            await self.tunneling_app_launching_error(error=e)

    async def _run_server(self):
        await self.before_server_launching()
        await self._server.run()

    async def _load_hook(self):
        self._hook = DefaultHook.load(self._options.hook_path, environment=self._env)
        await self.hook_loaded(hook=self._hook)

    @property
    def hook(self) -> Hook:
        return self._hook

    @property
    def server(self) -> LocalWebsocketServer:
        return self._server

    @property
    def options(self) -> Options:
        return self._options

    @property
    def environment(self) -> Environment:
        return self._env

    async def run(self):
        if self._options.use_tunneling_app:
            await self._run_tunneling_app()
        else:
            await self.public_url_unspecified_error()

        self._env.public_url = url.convert_url(self._options.public_url)

        self._options.save()

        await self._load_hook()
        await self._run_server()

    async def stop(self):
        await self.server.stop()
        if self._tunneling_app:
            await self._tunneling_app.stop()
