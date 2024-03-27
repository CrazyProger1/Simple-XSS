import flet as ft

from .exceptions import ValidationError
from .types import (
    BaseComponentManager,
    BaseComponent
)
from .channels import GUIChannel
from .contexts import Context
from ..channels import UIChannel


class ComponentManager(BaseComponentManager):
    def __init__(
            self,
            page: ft.Page,
            component: BaseComponent,
            context: Context,
    ):
        self._page = page
        self._component = component
        BaseComponent.context = context

        GUIChannel.need_update.subscribe(self._update_comps)
        GUIChannel.process_launched.subscribe(self._handle_process_launched)
        GUIChannel.process_terminated.subscribe(self._handle_process_terminated)

    async def _handle_process_launched(self):
        try:
            await self._validate_comps()
        except ValidationError as e:
            print(f'Validation Error Occurred BANNER: {e}')
            return
        await self._save_comps()
        await self._update_comps()
        await UIChannel.process_launched.publish_async()

    async def _handle_process_terminated(self):
        await self._update_comps()
        await UIChannel.process_terminated.publish_async()

    async def _setup_comps(self):
        for component in BaseComponent.components:
            await component.setup_async()

    async def _update_comps(self):
        for component in BaseComponent.components:
            await component.update_async()

    async def _validate_comps(self):
        for component in BaseComponent.components:
            await component.validate_async()

    async def _save_comps(self):
        for component in BaseComponent.components:
            await component.save_async()

    async def show(self):
        await self._page.add_async(self._component.build())
        await self._setup_comps()
        await self._update_comps()

    async def hide(self):
        await self._page.clean_async()
        await self._page.update_async()
