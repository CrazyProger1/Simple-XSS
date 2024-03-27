from simplexss.core.data import Environment
from simplexss.core.io import BaseIOManagerAPI
from simplexss.core.transports import (
    TransportServiceFactory,
    BaseTransportService,
    BaseSession as BaseTransportSession,
)
from simplexss.core.tunneling import (
    TunnelingServiceFactory,
    BaseTunnelingService,
    BaseSession as BaseTunnelingSession,
)
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


class SimpleXSSProcessor(BaseProcessor):
    def __init__(
            self,
            arguments: ArgumentsSchema,
            settings: SettingsSchema,
            transport_factory: TransportServiceFactory,
            tunneling_factory: TunnelingServiceFactory,
            hook_manager: BasePackageManager,
            payload_manager: BasePackageManager,
            io_manager: BaseIOManagerAPI
    ):
        self._arguments = arguments
        self._settings = settings
        self._transport_factory = transport_factory
        self._tunneling_factory = tunneling_factory
        self._hook_manager = hook_manager
        self._payload_manager = payload_manager
        self._io_manager = io_manager

        self._hook: BaseHook | None = None
        self._payload: BasePayload | None = None
        self._transport_service: BaseTransportService | None = None
        self._transport_session: BaseTransportSession | None = None
        self._tunneling_service: BaseTunnelingService | None = None
        self._tunneling_session: BaseTunnelingSession | None = None
        self._environment: Environment | None = None

    def _create_environment(self):
        self._environment = Environment(
            url=self._tunneling_session.public_url
        )

    def _load_hook(self):
        self._hook = self._hook_manager.get_package(
            self._settings.hook.current,
        )

    def _load_payload(self):
        self._payload = self._payload_manager.get_package(
            self._settings.payload.current
        )

    async def _run_tunneling(self):
        self._tunneling_service = self._tunneling_factory.create(
            self._settings.tunneling.current,
        )

        self._tunneling_session = await self._tunneling_service.run(
            self._transport_service.PROTOCOL,
            self._settings.transport.port,
        )

    async def _run_transport(self):
        self._transport_service = self._transport_factory.create(
            self._settings.transport.current
        )

        self._transport_session = await self._transport_service.run(
            host=self._settings.transport.host,
            port=self._settings.transport.port,
        )

    async def run(self):
        self._load_hook()
        self._load_payload()
        await self._run_transport()
        self._transport_session.api.bind_payload(self._payload.payload)
        await self._run_tunneling()
        self._create_environment()
        self._transport_session.api.bind_environment(self._environment)
        self._payload.bind_dependencies(
            env=self._environment,
            transport=self._transport_session.api,
            io=self._io_manager
        )
        self._payload.bind_endpoints()

    async def stop(self):
        await self._transport_service.stop(self._transport_session)
        await self._tunneling_service.stop(self._tunneling_session)
