import flet as ft

from simplexss.core.schemas import SettingsSchema
from simplexss.core.transports import BaseTransportServiceFactory
from simplexss.utils.packages import PackageManager
from .constants import (
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE,
    BOX_BORDER_RADIUS,
    BOX_BORDER,
    BOX_PADDING
)
from .enums import Messages
from ..exceptions import ValidationError
from ..types import (
    BaseComponent,
)


class HookBox(BaseComponent):
    def __init__(
            self,
            manager: PackageManager,
            transport_factory: BaseTransportServiceFactory,
    ):
        self._transport_factory = transport_factory
        self._manager = manager
        self._hook_name_text = ft.Text(
            value=Messages.HOOK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._hook_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,

        )

        self._hook_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self._hook_author_text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            italic=True
        )
        self._container = ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._hook_name_text
                        ]
                    ),
                    ft.Row(
                        controls=[
                            self._hook_dropdown,
                        ]
                    ),
                    self._hook_description_text,
                    ft.Container(
                        content=self._hook_author_text,
                        alignment=ft.alignment.bottom_right,

                    )
                ]
            )
        )

    async def setup_async(self):
        self._hook_dropdown.value = self.context.settings.hook.current
        await self.update_async()

    async def update_async(self):
        self._container.disabled = self.context.process_running
        self._hook_dropdown.options = [
            ft.dropdown.Option(hook.NAME)
            for hook in self._manager.packages
            if self.context.settings.transport.current in hook.TRANSPORTS
        ]
        await self._container.update_async()

    async def validate_async(self):
        if self._hook_dropdown.value is None:
            raise ValidationError('Please choose hook')

    async def save_async(self):
        self.context.settings.hook.current = self._hook_dropdown.value

    def build(self):
        return self._container
