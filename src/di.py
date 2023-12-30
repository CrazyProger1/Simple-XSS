from src.arguments.schemas import DefaultArgumentsSchema
from src.arguments.dependencies import arguments_parser, arguments_schema
from src.settings.schemas import DefaultSettingsSchema
from src.settings.dependencies import settings_schema
from src.plugins.dependencies import plugin_manager, plugin_loader
from src.plugins.managers import PluginManager
from src.core.dependencies import current_launcher
from src.core.launchers import Launcher
from src.utils import di, arguments, packages


def configurate_base_dependencies():
    di.injector.bind(arguments_schema, DefaultArgumentsSchema)
    di.injector.bind(settings_schema, DefaultSettingsSchema)

    di.injector.bind(
        arguments_parser,
        arguments.SchemedArgumentParser(
            schema=di.injector.get_dependency(arguments_schema)
        )
    )
    di.injector.bind(plugin_manager, PluginManager())
    di.injector.bind(plugin_loader, packages.PackageLoader())
    di.injector.bind(current_launcher, Launcher())
