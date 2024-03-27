import flet as ft

from simplexss.core.io import (
    BaseIOManagerAPI,
    Color
)
from .constants import (
    MESSAGE_SPACING,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    MESSAGE_FONT_SIZE,
    ICON_SIZE
)
from .enums import Messages
from ..types import BaseComponent


class MessageAreaBox(BaseComponent):
    def __init__(self, io_manager: BaseIOManagerAPI):
        self._io_manager = io_manager
        self._io_manager.add_sink(self._sink)
        self._message_list_view = ft.ListView(
            expand=True,
            spacing=MESSAGE_SPACING,
            auto_scroll=True,
        )
        self._content = ft.Row(
            expand=True,
            controls=[
                ft.Container(
                    content=self._message_list_view,
                    border=BOX_BORDER,
                    border_radius=BOX_BORDER_RADIUS,
                    padding=BOX_PADDING,
                    expand=True,
                )
            ]
        )

    async def _sink(self, message: str, color: Color):
        pass

    async def update_async(self):
        self._content.disabled = not self.context.process_running

    def build(self):
        return self._content


class MessageControlBox(BaseComponent):
    def __init__(self, io_manager: BaseIOManagerAPI):
        self._io_manager = io_manager
        self._input_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.MESSAGE,
            disabled=True
        )
        self._send_button = ft.IconButton(
            icon=ft.icons.SEND,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.BLUE_200,
            tooltip=Messages.SEND,
            disabled=True,
        )
        self._content = ft.Row(
            controls=[
                self._input_field,
                self._send_button
            ]
        )

    def build(self):
        return self._content
