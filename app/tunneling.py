from pyngrok import ngrok, exception as ngexecptions
from loguru import logger
from app.utils import observer
from app.exceptions import HTTPTunnelError
from app.validators import validate_port, validate_host


class HTTPTunnelingAppWrapper:
    """A wrapper for a tunneling application such as ngrok"""

    _app: str = None
    launched = observer.AsyncEvent()
    stopped = observer.AsyncEvent()

    def __init__(self, host: str, port: int):
        validate_host(host)
        validate_port(port)
        self._host = host
        self._port = port

    @classmethod
    def get_wrapper(cls, app: str) -> type["HTTPTunnelingAppWrapper"] | None:
        """Returns the tunneling application wrapper, if it exists"""

        for subcls in cls.__subclasses__():
            if subcls._app == app:
                return subcls

    @classmethod
    @property
    def app(cls):
        return cls._app

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def public_url(self) -> str:
        raise NotImplementedError

    async def run(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError


class NgrokWrapper(HTTPTunnelingAppWrapper):
    _app: str = 'ngrok'

    def __init__(self, *args, **kwargs):
        self._public_url = None
        self._tunnel = None
        super().__init__(*args, **kwargs)

    @property
    def public_url(self) -> str | None:
        return self._public_url

    async def run(self):
        try:
            self._tunnel = ngrok.connect(self.port)
            self._public_url = self._tunnel.public_url
            logger.info(f'Tunneling app is up: {self.host}:{self.port} -> {self._public_url}')
            await self.launched(public_url=self._public_url)
        except ngexecptions.PyngrokNgrokError as e:
            logger.error(f'Failed to open tunnel: {e.__class__.__name__}: {e}')
            raise HTTPTunnelError(self.host, self.port)

    async def stop(self):
        ngrok.disconnect(self.public_url)
        ngrok.kill()
        logger.info(f'Tunneling app is down: {self.host}:{self.port} -> {self._public_url}')
        await self.stopped(public_url=self.public_url)
