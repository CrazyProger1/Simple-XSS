from src.logging.services import configurate_logging
from src.arguments.schemas import DefaultArgumentsSchema
from src.arguments.services import parse_arguments
from src.arguments.dependencies import arguments_parser, arguments_schema
from src.settings.schemas import DefaultSettingsSchema
from src.settings.services import load_settings
from src.settings.dependencies import settings_schema
from src.plugins.dependencies import plugin_manager, plugin_loader
from src.plugins.managers import PluginManager
from src.plugins.services import load_plugins
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


def main():
    configurate_logging()
    configurate_base_dependencies()
    load_plugins()
    parse_arguments()
    load_settings()


if __name__ == '__main__':
    main()
