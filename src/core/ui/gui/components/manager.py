import asyncio

import flet as ft

from src.utils import di, clsutils
from src.core.data import (
    DataDependencyContainer,
    Context,
    DataEventChannel
)

from .types import (
    BaseComponentManager,
    CustomControl
)
from .dependencies import (
    ComponentsDependencyContainer,
    configure_components_dependencies
)


class ComponentManager(BaseComponentManager):
    def __init__(self):
        from ..events import GUIEventChannel
        from src.core.logic import LogicEventChannel

        configure_components_dependencies()
        self._page: ft.Page | None = None
        self.setup_controls()

        GUIEventChannel.process_activated.add_listener(self._handle_process_activated)
        GUIEventChannel.process_deactivated.add_listener(self._handle_process_deactivated)
        LogicEventChannel.error_occurred.add_listener(self._handle_error)
        GUIEventChannel.internal_error_occurred.add_listener(self._handle_error)
        DataEventChannel.context_changed.add_listener(self.update_controls)

    @di.inject
    def _handle_error(self, error, banner=ComponentsDependencyContainer.error_banner):
        asyncio.create_task(banner.show(self._page, error))

    async def _handle_process_deactivated(self):
        from src.core.ui import UIEventChannel

        await UIEventChannel.process_deactivated()

    async def _handle_process_activated(self):
        from src.core.ui import UIEventChannel

        all_valid = self.validate_controls()

        if all_valid:
            self.save_controls()
            await UIEventChannel.process_activated()

    @di.inject
    def setup_controls(self, context: Context = DataDependencyContainer.context):
        for control in clsutils.iter_instances(CustomControl):
            control.setup(context=context)

    @di.inject
    def update_controls(
            self,
            context: Context = DataDependencyContainer.context
    ):
        for control in clsutils.iter_instances(CustomControl):
            control.update(context=context)
        asyncio.create_task(self._page.update_async())

    @di.inject
    def validate_controls(self, context: Context = DataDependencyContainer.context) -> bool:
        results = []
        for control in clsutils.iter_instances(CustomControl):
            results.append(control.validate(context=context))

        return all(results)

    @di.inject
    def save_controls(self, context: Context = DataDependencyContainer.context):
        for control in clsutils.iter_instances(CustomControl):
            control.save(context=context)

    @di.inject
    async def show(self, page: ft.Page, main_box=ComponentsDependencyContainer.main_box):
        self._page = page
        page.overlay.extend(CustomControl.overlay)
        self.update_controls()
        await page.add_async(main_box.build())
