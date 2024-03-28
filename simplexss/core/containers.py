from simplexss.core.ui.contexts import UIContext
from simplexss.utils.packages import PackageManager
from simplexss.core.tunneling import TunnelingServiceFactory
from simplexss.core.transports import TransportServiceFactory
from simplexss.core.ui import UIFactory
from simplexss.core.io import IOManagerAPI
from simplexss.core.process import SimpleXSSProcessor
from simplexss.utils.di import (
    containers,
    dependencies
)
from simplexss.utils.arguments import (
    SchemedArgumentParser
)
from simplexss.utils.settings.toml import (
    TOMLLoader,
)
from simplexss.core.core import Core
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from simplexss.core.types import (
    BaseHook,
    BasePlugin,
    BasePayload
)


class CoreContainer(containers.Container):
    arguments_schema = dependencies.Dependency(ArgumentsSchema)
    settings_schema = dependencies.Dependency(SettingsSchema)

    arguments_parser = dependencies.Factory(SchemedArgumentParser, kwargs={'schema': arguments_schema})
    settings_loader = dependencies.Factory(TOMLLoader)

    arguments = dependencies.Dependency()
    settings = dependencies.Dependency()

    plugin_class = dependencies.Dependency(BasePlugin)
    plugin_manager = dependencies.Singleton(PackageManager)

    hook_class = dependencies.Dependency(BaseHook)
    hook_manager = dependencies.Singleton(PackageManager)

    payload_class = dependencies.Dependency(BasePayload)
    payload_manager = dependencies.Singleton(PackageManager)

    ui_factory = dependencies.Factory(UIFactory)

    tunneling_service_factory = dependencies.Factory(TunnelingServiceFactory)
    transport_service_factory = dependencies.Factory(TransportServiceFactory)

    io_manager = dependencies.Singleton(IOManagerAPI)

    ui_context = dependencies.Singleton(
        UIContext,
        kwargs={
            'settings': settings,
            'arguments': arguments
        }
    )

    processor = dependencies.Factory(
        SimpleXSSProcessor,
        kwargs={
            'arguments': arguments,
            'settings': settings,
            'transport_factory': transport_service_factory,
            'tunneling_factory': tunneling_service_factory,
            'hook_manager': hook_manager,
            'payload_manager': payload_manager,
            'io_manager': io_manager,
            'ui_context': ui_context
        }
    )

    core = dependencies.Singleton(
        Core,
        kwargs={
            'arguments': arguments,
            'settings': settings,
            'ui_factory': ui_factory,
            'processor': processor
        }
    )
