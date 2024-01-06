from src.utils import di, argutil, packages, io

from .payloads.dependencies import payload_loader
from .plugins.dependencies import plugin_manager, plugin_loader
from .arguments.dependencies import argument_parser
from .context.dependencies import context_class
from .hooks.dependencies import hook_loader
from .settings.dependencies import settings_scheme
from .transports.dependencies import transport_service_factory
from .tunneling.dependencies import tunneling_service_factory

from .arguments import DefaultArgumentsScheme
from .settings import DefaultSettingsScheme
from .plugins import PluginManager
from .context import DefaultContext
from .tunneling import TunnelingServiceFactory
from .transports import TransportServiceFactory

io_manager = di.Dependency(io.BaseIOManager)


def configurate_base_dependencies():
    """
    Configures the base dependencies using the dependency injection (DI) framework.
    """

    di.injector.bind(argument_parser, argutil.SchemedArgumentParser(
        schema=DefaultArgumentsScheme
    ))

    di.injector.bind(plugin_manager, PluginManager())
    di.injector.bind(plugin_loader, packages.PackageLoader())

    di.injector.bind(settings_scheme, DefaultSettingsScheme)

    di.injector.bind(hook_loader, packages.PackageLoader())
    di.injector.bind(payload_loader, packages.PackageLoader())

    di.injector.bind(context_class, DefaultContext)

    di.injector.bind(io_manager, io.AsyncIOManager())

    di.injector.bind(transport_service_factory, TransportServiceFactory())
    di.injector.bind(tunneling_service_factory, TunnelingServiceFactory())
