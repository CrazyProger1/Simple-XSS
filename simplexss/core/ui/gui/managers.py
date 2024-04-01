import flet as ft

from simplexss.core.ui.contexts import UIContext
from .exceptions import ValidationError
from .types import (
    BaseComponentManager,
    BaseComponent,
    BaseBanner,
)
from .channels import GUIChannel
from ..channels import UIChannel


class ComponentManager(BaseComponentManager):
    def __init__(
            self,
            page: ft.Page,
            component: BaseComponent,
            context: UIContext,
            error_banner: BaseBanner,
            warning_banner: BaseBanner
    ):
        self._page = page
        self._component = component
        self._error_banner = error_banner
        self._warning_banner = warning_banner
        self._context = context

        BaseComponent.page = page
        BaseComponent.context = context

        GUIChannel.need_update.subscribe(self._update_comps)
        GUIChannel.process_launched.subscribe(self._handle_process_launched)
        GUIChannel.process_terminated.subscribe(self._handle_process_terminated)
        UIChannel.show_error.subscribe(self._handle_error)

    async def _handle_process_launched(self):
        self._context.process_running = True
        try:
            await self._validate_comps()
        except ValidationError as e:
            await self._error_banner.show(self._page, str(e))
            self._context.process_running = False
            await self._update_comps()
            return
        await self._save_comps()
        await self._update_comps()
        await UIChannel.process_launched.publish_async()

    async def _handle_process_terminated(self):
        self._context.process_running = False
        await self._update_comps()
        await UIChannel.process_terminated.publish_async()

    async def _handle_error(self, error: str):
        self._context.process_running = False
        await self._error_banner.show(self._page, error)
        await self._update_comps()

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
