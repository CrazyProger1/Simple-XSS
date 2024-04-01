import os

from simplexss.core.config import (
    PAYLOAD_FILE,
    HOOK_FILE,
)
from simplexss.core.logging import logger
from simplexss.core.schemas import SettingsSchema
from simplexss.core.containers import CoreContainer
from simplexss.core.config import (
    PLUGINS_DIRECTORY,
    PLUGIN_FILE
)
from simplexss.utils.di import inject
from simplexss.utils.packages import (
    BasePackage,
    BasePackageManager
)


@inject
def load_plugins(
        cls: BasePackage = CoreContainer.plugin_class,
        manager: BasePackageManager = CoreContainer.plugin_manager
):
    os.makedirs(PLUGINS_DIRECTORY, exist_ok=True)

    manager.load_packages(
        PLUGINS_DIRECTORY,
        class_name='Plugin',
        base_class=cls,
        file=PLUGIN_FILE,
    )
    logger.info(f'Plugins loaded')


@inject
def load_hooks(
        cls: BasePackage = CoreContainer.hook_class,
        manager: BasePackageManager = CoreContainer.hook_manager,
        settings: SettingsSchema = CoreContainer.settings
):
    os.makedirs(settings.hook.directory, exist_ok=True)

    manager.load_packages(
        settings.hook.directory,
        class_name='Hook',
        base_class=cls,
        file=HOOK_FILE,
    )
    logger.info('Hooks loaded')


@inject
def load_payloads(
        cls: BasePackage = CoreContainer.payload_class,
        manager: BasePackageManager = CoreContainer.payload_manager,
        settings: SettingsSchema = CoreContainer.settings
):
    os.makedirs(settings.payload.directory, exist_ok=True)

    manager.load_packages(
        settings.payload.directory,
        class_name='Payload',
        base_class=cls,
        file=PAYLOAD_FILE,
    )
    logger.info('Payloads loaded')
