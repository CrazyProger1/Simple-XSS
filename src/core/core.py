import sys

from src.utils import di
from .events import (
    application_initialized,
    application_launched,
    application_terminated,
    async_mode_entered,
    arguments_parsed,
    settings_loaded,
    plugins_loaded
)

from .logic import run_logic
from .dependencies import (
    configurate_base_dependencies,
    argument_parser,
    current_arguments,
    current_settings,
    plugin_loader,
    plugin_manager,
    settings_scheme
)
from .services import arguments, plugins, settings
from .ui import run_ui


@di.injector.inject
def parse_arguments(parser=argument_parser):
    args = arguments.parse_arguments(parser=parser, args=sys.argv[1:])
    di.injector.bind(current_arguments, args)


@di.injector.inject
def load_plugins(
        manager=plugin_manager,
        loader=plugin_loader):
    plugins.load_plugins(manager=manager, loader=loader)


@di.injector.inject
def load_settings(
        scheme: type[settings.DefaultSettingsScheme] = settings_scheme,
        args: arguments.DefaultArgumentsScheme = current_arguments):
    loaded_settings = settings.load_settings(scheme=scheme, file=args.settings_file)
    di.injector.bind(current_settings, loaded_settings)


def initialize():
    configurate_base_dependencies()

    load_plugins()
    plugins_loaded()

    parse_arguments()
    arguments_parsed()

    load_settings()
    settings_loaded()

    async_mode_entered.add_listener(run_logic)


def run():
    application_launched()

    # Init stage
    initialize()
    application_initialized()

    # UI launch stage
    run_ui()

    application_terminated()
