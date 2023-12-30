from src.arguments.schemes import DefaultArgumentsScheme
from src.arguments.dependencies import arguments_parser, arguments_schema, current_arguments
from src.settings.schemes import DefaultSettingsScheme
from src.settings.dependencies import settings_schema
from src.plugins.dependencies import plugin_manager, plugin_loader
from src.plugins.managers import PluginManager
from src.core.dependencies import current_launcher
from src.core.launchers import Launcher
from src.utils import di, arguments, packages
from src.core.view.dependencies import current_ui
from src.core.view.ui import get_ui
from src.core.controller.controllers import Controller
from src.core.controller.dependencies import current_controller


def configurate_base_dependencies():
    di.injector.bind(arguments_schema, DefaultArgumentsScheme)
    di.injector.bind(settings_schema, DefaultSettingsScheme)

    di.injector.bind(
        arguments_parser,
        arguments.SchemedArgumentParser(
            schema=di.injector.get_dependency(arguments_schema)
        )
    )
    di.injector.bind(plugin_manager, PluginManager())
    di.injector.bind(plugin_loader, packages.PackageLoader())
    di.injector.bind(current_launcher, Launcher())


@di.injector.inject
def configurate_launcher_dependencies(args: DefaultArgumentsScheme = current_arguments):
    di.injector.bind(current_ui, get_ui(args.graphic_mode))
    di.injector.bind(current_controller, Controller())
