from simplexss.core.data import Environment
from simplexss.core.io import BaseIOManagerAPI
from simplexss.core.transports import (
    TransportServiceFactory,
    BaseTransportService,
    BaseSession as BaseTransportSession,
)
from simplexss.core.transports.exceptions import TransportError
from simplexss.core.tunneling import (
    TunnelingServiceFactory,
    BaseTunnelingService,
    BaseSession as BaseTunnelingSession,
)
from simplexss.core.tunneling.exceptions import TunnelingError
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from simplexss.core.types import (
    BasePayload,
    BaseHook,
)
from simplexss.utils.packages import BasePackageManager
from .types import BaseProcessor
from .channels import ProcessorChannel
from .logging import logger
from .enums import Messages
from simplexss.core.ui.contexts import UIContext


class SimpleXSSProcessor(BaseProcessor):
    def __init__(
            self,
            arguments: ArgumentsSchema,
            settings: SettingsSchema,
            transport_factory: TransportServiceFactory,
            tunneling_factory: TunnelingServiceFactory,
            hook_manager: BasePackageManager,
            payload_manager: BasePackageManager,
            io_manager: BaseIOManagerAPI,
            ui_context: UIContext
    ):
        self._arguments = arguments
        self._settings = settings
        self._transport_factory = transport_factory
        self._tunneling_factory = tunneling_factory
        self._hook_manager = hook_manager
        self._payload_manager = payload_manager
        self._io_manager = io_manager
        self._ui_context = ui_context

        self._hook: BaseHook | None = None
        self._payload: BasePayload | None = None
        self._transport_service: BaseTransportService | None = None
        self._transport_session: BaseTransportSession | None = None
        self._tunneling_service: BaseTunnelingService | None = None
        self._tunneling_session: BaseTunnelingSession | None = None
        self._environment: Environment | None = None

    def _setup_environment(self):
        self._environment = Environment(
            settings=self._settings,
            arguments=self._arguments
        )

    def _setup_hook(self):
        self._hook = self._hook_manager.get_package(
            self._settings.hook.current,
        )

    def _setup_payload(self):
        self._payload = self._payload_manager.get_package(
            self._settings.payload.current
        )

    def _setup_tunneling(self):
        self._tunneling_service = self._tunneling_factory.create(
            self._settings.tunneling.current,
        )

    def _setup_transport(self):
        self._transport_service = self._transport_factory.create(
            self._settings.transport.current
        )

    async def _run_tunneling(self):
        try:
            self._tunneling_session = await self._tunneling_service.run(
                self._transport_service.PROTOCOL,
                self._settings.transport.port,
            )
        except TunnelingError as e:
            await ProcessorChannel.error_occurred.publish_async(error=f'Tunneling Error: {e}')
            raise

    async def _run_transport(self):
        try:
            settings = self._settings.transport

            self._transport_session = await self._transport_service.run(
                host=settings.host,
                port=settings.port,
            )
        except TransportError as e:
            await ProcessorChannel.error_occurred.publish_async(error=f'Transport Error: {e}')
            raise

    async def _bind_dependencies(self):

        if self._settings.tunneling.use:
            self._environment.url = self._tunneling_session.public_url
        else:
            url = self._settings.tunneling.public_url

            if not url:
                url = f'http://{self._transport_session.host}:{self._transport_session.port}'

            self._environment.url = url

        self._hook.bind_dependencies(
            env=self._environment,
            io=self._io_manager,
        )
        self._ui_context.hook = self._hook.hook

        self._transport_session.api.bind_payload(self._payload.payload)
        self._transport_session.api.bind_environment(self._environment)
        self._payload.bind_dependencies(
            env=self._environment,
            transport=self._transport_session.api,
            io=self._io_manager
        )
        self._payload.bind_endpoints()

    async def _setup(self):
        self._setup_environment()
        self._setup_hook()
        self._setup_payload()
        self._setup_transport()
        self._setup_tunneling()

    async def _run(self):
        await self._run_transport()

        if self._settings.tunneling.use:
            await self._run_tunneling()

    async def run(self):
        try:
            await self._setup()
            await self._run()
            await self._bind_dependencies()
            await ProcessorChannel.process_launched.publish_async()

            logger.info('Process launched')
            await self._io_manager.print(Messages.PROCESS_LAUNCHED, color='green')
        except Exception as e:
            await self.stop()

    async def stop(self):
        try:
            await self._transport_service.stop(self._transport_session)

            if self._settings.tunneling.use:
                await self._tunneling_service.stop(self._tunneling_session)

            await ProcessorChannel.process_terminated.publish_async()

            logger.info('Process terminated')
            await self._io_manager.print(Messages.PROCESS_TERMINATED, color='green')
        except Exception as e:
            pass
