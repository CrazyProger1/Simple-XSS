from src.utils import io

from src.core import (
    arguments,
    settings,
    plugins,
    payloads,
    hooks,
    io,
    tunneling
)


def configure_base_dependencies():
    """
    Configures the base dependencies using the dependency injection (DI) framework.
    """

    arguments.ArgumentsDependencyContainer.configure()
    settings.SettingsDependencyContainer.configure()
    plugins.PluginsDependencyContainer.configure()
    payloads.PayloadsDependencyContainer.configure()
    hooks.HooksDependencyContainer.configure()
    io.IODependencyContainer.configure()
    tunneling.TunnelingDependencyContainer.configure()
