import flet as ft

from simplexss.core.schemas import SettingsSchema
from simplexss.utils.packages import PackageManager
from .constants import (
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE
)
from .enums import Messages
from ..exceptions import ValidationError
from ..types import (
    BaseComponent,
)


class PayloadBox(BaseComponent):
    def __init__(self, manager: PackageManager):
        self._manager = manager

        self._payload_name_text = ft.Text(
            value=Messages.PAYLOAD,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._payload_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,

        )
        self._payload_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self._payload_author_text = ft.Text(
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
                            self._payload_name_text
                        ]
                    ),
                    ft.Row(
                        controls=[
                            self._payload_dropdown,
                        ]
                    ),
                    self._payload_description_text,
                    ft.Container(
                        content=self._payload_author_text,
                        alignment=ft.alignment.bottom_right,

                    )
                ]
            )
        )

    async def setup_async(self):
        self._payload_dropdown.options = [
            ft.dropdown.Option(payload.NAME)
            for payload in self._manager.packages
        ]
        self._payload_dropdown.value = self.context.settings.payload.current

    async def update_async(self):
        self._container.disabled = self.context.process_running
        await self._container.update_async()

    async def validate_async(self):
        if self._payload_dropdown.value is None:
            raise ValidationError('Please choose payload')

    def build(self):
        return self._container
