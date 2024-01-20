from loguru import logger

from src.utils import di, io
from src.core.io import IODependencyContainer
from src.core.data import (
    DataDependencyContainer,
    Context,
    Environment
)
from src.core.transports import TransportsDependencyContainer
from src.core.tunneling import TunnelingDependencyContainer
from src.core.hooks import load_hook
from src.core.payloads import load_payload

from .types import BaseProcess
from .enums import Messages


class Process(BaseProcess): # TO REFACTOR!!!!!!!!!!!!!!!!
    @di.inject
    def __init__(
            self,
            io_manager: io.AsyncIOManager = IODependencyContainer.io_manager,
            context: Context = DataDependencyContainer.context,
            env: Environment = DataDependencyContainer.environment
    ):
        self._io = io_manager
        self._context = context
        self._hook = None
        self._payload = None
        self._transport_service = None
        self._tunneling_service = None
        self._protocol = None
        self._tunneling_session = None
        self._transport_session = None
        self._env = env

    @staticmethod
    def _raise_error(error: str):
        from src.core.logic import LogicEventChannel

        LogicEventChannel.error_occurred(error=error)
        raise RuntimeError(error)

    async def _validate_hook(self):
        if self._hook.TRANSPORT != self._protocol:
            self._raise_error(Messages.HOOK_NOT_SUPPORTS_PROTOCOL_ERROR.format(protocol=self._protocol.value))

    async def _validate_payload(self):
        if self._protocol not in self._payload.TRANSPORTS:
            self._raise_error(Messages.PAYLOAD_NOT_SUPPORTS_PROTOCOL_ERROR.format(protocol=self._protocol.value))

    async def _load_hook(self):
        try:
            self._hook = load_hook(
                self._context.settings.hook.current.unwrap()
            )
            self._hook.io = self._io
            self._env.hook = self._hook
            await self._io.info(Messages.HOOK_LOADED.format(
                name=self._hook.NAME,
                version=self._hook.VERSION
            ))
        except Exception as e:
            self._raise_error(
                Messages.HOOK_LOADING_ERROR.format(
                    details=f'{e.__class__.__name__}: {e}'
                )
            )

    async def _load_payload(self):
        try:
            self._payload = load_payload(
                self._context.settings.payload.current.unwrap()
            )
            self._payload.io = self._io
            self._env.payload = self._payload
            await self._io.info(Messages.PAYLOAD_LOADED.format(
                name=self._payload.NAME,
                version=self._payload.VERSION
            ))
        except Exception as e:
            self._raise_error(Messages.PAYLOAD_LOADING_ERROR.format(
                details=f'{e.__class__.__name__}: {e}'
            ))

    @di.inject
    async def _run_transport(self, factory=TransportsDependencyContainer.factory):
        transport_settings = self._context.settings.transport.unwrap()
        self._transport_service = factory.create(transport_settings.current)
        self._protocol = self._transport_service.protocol
        await self._validate_hook()
        await self._validate_payload()
        self._transport_session = await self._transport_service.run(
            host=transport_settings.host,
            port=transport_settings.port
        )
        self._transport_session.add_listener(self._payload.on_event)
        await self._io.info(Messages.TRANSPORT_LAUNCHED.format(
            host=transport_settings.host,
            port=transport_settings.port
        ))

    @di.inject
    async def _run_tunneling(self, factory=TunnelingDependencyContainer.factory):
        transport_settings = self._context.settings.transport.unwrap()
        tunneling_settings = self._context.settings.tunneling.unwrap()
        if tunneling_settings.use:
            self._tunneling_service = factory.create(tunneling_settings.current)
            self._tunneling_session = await self._tunneling_service.run(
                protocol=self._protocol,
                port=transport_settings.port
            )
            self._context.settings.tunneling.public_url = self._tunneling_session.public_url
            await self._io.info(Messages.TUNNEL_ESTABLISHED.format(
                url=self._tunneling_session.public_url
            ))

    async def _stop_transport(self):
        try:
            await self._transport_service.stop(self._transport_session)
            await self._io.info(Messages.TRANSPORT_STOPPED)
        except Exception:
            pass

    async def _stop_tunneling(self):
        try:
            await self._io.info(Messages.TUNNELING_STOPPED)
            await self._tunneling_service.stop(self._tunneling_session)
        except Exception:
            pass

    @logger.catch
    async def _call_on_stop(self):
        await self._hook.on_stopped(self._env)
        await self._payload.on_stopped(self._env)

    @logger.catch
    async def _call_on_launched(self):
        await self._hook.on_launched(self._env)
        await self._payload.on_launched(self._env)

    async def activate(self):
        await self._io.info(Messages.LAUNCHING)
        self._context.process_active = True

        try:
            await self._load_hook()
            await self._load_payload()

            await self._run_transport()
            await self._run_tunneling()

            await self._call_on_launched()

            self._context.hook_code = self._hook.hook
        except RuntimeError:
            await self.deactivate()

    async def deactivate(self):
        await self._io.info(Messages.TERMINATING)
        self._context.process_active = False

        await self._stop_transport()
        await self._stop_tunneling()

        await self._call_on_stop()
