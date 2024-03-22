from simplexss.utils.packages import PackageManager
from simplexss.core.tunneling import TunnelingServiceFactory
from simplexss.core.transports import TransportServiceFactory
from simplexss.core.ui import UIFactory
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
from simplexss.core.plugins import Plugin
from simplexss.core.payloads import Payload
from simplexss.core.hooks import Hook


class CoreContainer(containers.Container):
    arguments_schema = dependencies.Dependency(ArgumentsSchema)
    settings_schema = dependencies.Dependency(SettingsSchema)

    arguments_parser = dependencies.Factory(SchemedArgumentParser, kwargs={'schema': arguments_schema})
    settings_loader = dependencies.Factory(TOMLLoader)

    arguments = dependencies.Dependency()
    settings = dependencies.Dependency()

    plugin_class = dependencies.Dependency(Plugin)
    plugin_manager = dependencies.Singleton(PackageManager)

    hook_class = dependencies.Dependency(Hook)
    hook_manager = dependencies.Singleton(PackageManager)

    payload_class = dependencies.Dependency(Payload)
    payload_manager = dependencies.Singleton(PackageManager)

    ui_factory = dependencies.Factory(UIFactory)

    tunneling_service_factory = dependencies.Factory(TunnelingServiceFactory)
    transport_service_factory = dependencies.Factory(TransportServiceFactory)

    core = dependencies.Singleton(Core, kwargs={
        'arguments': arguments,
        'settings': settings,
        'ui_factory': ui_factory,
    })
