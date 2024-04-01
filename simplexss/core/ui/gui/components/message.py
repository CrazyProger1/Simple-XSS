import asyncio

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
    ICON_SIZE,
    COLOR_TABLE
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

    async def _add_text(self, text: ft.Text):
        self._message_list_view.controls.append(text)
        await self._message_list_view.update_async()

    async def _sink(self, message: str, color: Color):
        await self._add_text(
            ft.Text(
                message,
                selectable=True,
                color=COLOR_TABLE.get(color if isinstance(color, str) else color, COLOR_TABLE[Color.DEFAULT]),
                size=MESSAGE_FONT_SIZE
            )
        )

    async def update_async(self):
        self._content.disabled = not self.context.process_running
        await self._content.update_async()

    def build(self):
        return self._content


class MessageControlBox(BaseComponent):
    def __init__(self, io_manager: BaseIOManagerAPI):
        self._io_manager = io_manager
        self._io_manager.set_source(self._source)
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
            on_click=self._handle_send
        )
        self._content = ft.Row(
            controls=[
                self._input_field,
                self._send_button
            ]
        )

        self._text_entered = False
        self._text = None

    async def _handle_send(self, e):
        self._text_entered = True
        self._text = self._input_field.value

    async def _source(self, prompt: str, color: Color):
        self._input_field.hint_text = prompt
        self._input_field.disabled = False
        self._send_button.disabled = False
        self._text_entered = False

        await self.update_async()

        while not self._text_entered:
            await asyncio.sleep(0.1)

        self._input_field.hint_text = Messages.MESSAGE
        self._input_field.disabled = True
        self._send_button.disabled = True
        self._input_field.value = None

        await self.update_async()

        await self._io_manager.print(f'{prompt}: {self._text}', color=color)

        return self._text

    async def update_async(self):
        await self._content.update_async()

    def build(self):
        return self._content
