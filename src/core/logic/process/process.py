from src.utils import di, io
from src.core.io import IODependencyContainer
from src.core.context import DefaultContext, ContextDependenciesContainer
from src.core.transports import TransportsDependencyContainer
from src.core.tunneling import TunnelingDependencyContainer
from src.core.hooks import load_hook
from src.core.payloads import load_payload

from .types import BaseProcess
from .enums import Messages


class Process(BaseProcess):
    @di.inject
    def __init__(
            self,
            io_manager: io.AsyncIOManager = IODependencyContainer.io_manager,
            context: DefaultContext = ContextDependenciesContainer.current_context
    ):
        self._io = io_manager
        self._context = context
        self._hook = None
        self._payload = None
        self._transport_service = None
        self._tunneling_service = None
        self._protocol = None
        self._tunneling_session = None
        self._transport_server = None

    async def _raise_error(self, error: str):
        from src.core.logic import LogicEventChannel
        LogicEventChannel.error_occurred(error=error)
        raise RuntimeError(error)

    async def _load_hook(self):
        try:
            self._hook = load_hook(
                self._context.settings.hook.current.unwrap()
            )
        except Exception as e:
            await self._raise_error(
                Messages.HOOK_LOADING_ERROR.format(
                    details=f'{e.__class__.__name__}: {e}'
                )
            )

    async def _load_payload(self):
        try:
            self._payload = load_payload(
                self._context.settings.payload.current.unwrap()
            )
        except Exception as e:
            await self._raise_error(Messages.PAYLOAD_LOADING_ERROR.format(
                details=f'{e.__class__.__name__}: {e}'
            ))

    @di.inject
    async def _run_transport(self, factory=TransportsDependencyContainer.factory):
        transport_settings = self._context.settings.transport.unwrap()
        self._transport_service = factory.create(transport_settings.current)
        self._protocol = self._transport_service.protocol
        self._transport_server = await self._transport_service.run(
            host=transport_settings.host,
            port=transport_settings.port
        )

    @di.inject
    async def _run_tunneling(self, factory=TunnelingDependencyContainer.factory):
        transport_settings = self._context.settings.transport.unwrap()
        tunneling_settings = self._context.settings.tunneling.unwrap()
        if tunneling_settings.use:
            self._tunneling_service = factory.create(tunneling_settings.current)
            await self._tunneling_service.run(
                protocol=self._protocol,
                port=transport_settings.port
            )

    async def _stop_transport(self):
        try:
            transport_settings = self._context.settings.transport.unwrap()
            await self._transport_service.stop(
                host=transport_settings.host,
                port=transport_settings.port
            )
        except AttributeError:
            pass

    async def _stop_tunneling(self):
        try:
            await self._tunneling_service.stop(self._tunneling_session)
        except AttributeError:
            pass

    async def activate(self):
        await self._io.info(Messages.LAUNCHING)
        self._context.process_active = True

        try:
            await self._load_hook()
            await self._load_payload()
            await self._run_transport()
            await self._run_tunneling()
        except RuntimeError:
            await self.deactivate()

    async def deactivate(self):
        await self._io.info(Messages.TERMINATING)
        self._context.process_active = False

        await self._stop_transport()
        await self._stop_tunneling()
