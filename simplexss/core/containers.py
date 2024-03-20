from simplexss.utils.di import (
    containers,
    dependencies
)
from simplexss.utils.args import (
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


class CoreContainer(containers.Container):
    arguments_schema = dependencies.Dependency(ArgumentsSchema)
    settings_schema = dependencies.Dependency(SettingsSchema)

    arguments_parser = dependencies.Factory(SchemedArgumentParser, kwargs={'schema': arguments_schema})
    settings_loader = dependencies.Factory(TOMLLoader)

    arguments = dependencies.Dependency()
    settings = dependencies.Dependency()

    core = dependencies.Singleton(Core, kwargs={'arguments': arguments, 'settings': settings})
