from pydantic import BaseModel

from src.utils import di, argutil, packages, io

current_arguments = di.Dependency(BaseModel)
argument_parser = di.Dependency(argutil.SchemedArgumentParser)

plugin_manager = di.Dependency(packages.PackageManager)
plugin_loader = di.Dependency(packages.PackageLoader)

settings_scheme = di.Dependency(BaseModel)
current_settings = di.Dependency(BaseModel)

context_class = di.Dependency(type)
current_context = di.Dependency(object)

hook_loader = di.Dependency(packages.PackageLoader)

payload_loader = di.Dependency(packages.PackageLoader)

io_manager = di.Dependency(io.BaseIOManager)


def configurate_base_dependencies():
    from .services import (
        arguments,
        plugins,
        settings,
        context
    )

    di.injector.bind(argument_parser, argutil.SchemedArgumentParser(
        schema=arguments.DefaultArgumentsScheme
    ))

    di.injector.bind(plugin_manager, plugins.PluginManager())
    di.injector.bind(plugin_loader, packages.PackageLoader())

    di.injector.bind(settings_scheme, settings.DefaultSettingsScheme)

    di.injector.bind(hook_loader, packages.PackageLoader())
    di.injector.bind(payload_loader, packages.PackageLoader())

    di.injector.bind(context_class, context.DefaultContext)

    di.injector.bind(io_manager, io.AsyncIOManager())
