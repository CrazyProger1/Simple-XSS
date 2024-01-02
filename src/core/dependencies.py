from pydantic import BaseModel

from src.utils import di, argutil, packages
from .services import arguments, plugins, settings

current_arguments = di.Dependency(BaseModel)
argument_parser = di.Dependency(argutil.SchemedArgumentParser)

plugin_manager = di.Dependency(packages.PackageManager)
plugin_loader = di.Dependency(packages.PackageLoader)

settings_scheme = di.Dependency(BaseModel)
current_settings = di.Dependency(BaseModel)


def configurate_base_dependencies():
    di.injector.bind(argument_parser, argutil.SchemedArgumentParser(
        schema=arguments.DefaultArgumentsScheme
    ))

    di.injector.bind(plugin_manager, plugins.PluginManager())
    di.injector.bind(plugin_loader, packages.PackageLoader())

    di.injector.bind(settings_scheme, settings.DefaultSettingsScheme)
