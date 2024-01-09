from src.utils import di, argutil, packages, io

from .payloads.dependencies import payload_loader_dependency
from .plugins.dependencies import plugin_manager_dependency, plugin_loader_dependency
from .arguments.dependencies import argument_parser_dependency
from .context.dependencies import context_class_dependency
from .hooks.dependencies import hook_loader_dependency
from .settings.dependencies import settings_scheme_dependency
from .transports.dependencies import transport_service_factory_dependency
from .tunneling.dependencies import tunneling_service_factory_dependency
from .io.dependencies import io_manager_dependency

from .arguments import DefaultArgumentsScheme
from .settings import DefaultSettingsScheme
from .plugins import PluginManager
from .context import DefaultContext
from .tunneling import TunnelingServiceFactory
from .transports import TransportServiceFactory


def configurate_base_dependencies():
    """
    Configures the base dependencies using the dependency injection (DI) framework.
    """

    di.injector.bind(argument_parser_dependency, argutil.SchemedArgumentParser(
        schema=DefaultArgumentsScheme
    ))

    di.injector.bind(plugin_manager_dependency, PluginManager())
    di.injector.bind(plugin_loader_dependency, packages.PackageLoader())

    di.injector.bind(settings_scheme_dependency, DefaultSettingsScheme)

    di.injector.bind(hook_loader_dependency, packages.PackageLoader())
    di.injector.bind(payload_loader_dependency, packages.PackageLoader())

    di.injector.bind(context_class_dependency, DefaultContext)

    di.injector.bind(io_manager_dependency, io.AsyncIOManager())

    di.injector.bind(transport_service_factory_dependency, TransportServiceFactory())
    di.injector.bind(tunneling_service_factory_dependency, TunnelingServiceFactory())
