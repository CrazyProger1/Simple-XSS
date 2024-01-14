import asyncio

import flet as ft

from src.utils import io, di
from src.core.io import IODependencyContainer
from .constants import (
    MESSAGE_SPACING,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    COLOR_TABLE,
    MESSAGE_FONT_SIZE, ICON_SIZE
)
from .utils import convert_color
from ..types import CustomControl
from ...enums import Messages


class MessageAreaBox(CustomControl):
    @di.inject
    def __init__(self, io_manager: io.BaseIOManager = IODependencyContainer.io_manager):
        self._io_manager = io_manager
        self._io_manager.print_source = self._handle_print

        self._message_list_view = ft.ListView(
            expand=True,
            spacing=MESSAGE_SPACING,
            auto_scroll=True,
        )

    async def _handle_print(self, *messages, sep: str = ' ', end: str = '\n', color=None):
        text = sep.join(messages)

        if end != '\n':
            text += end

        await self.add_text(
            text=ft.Text(
                value=text,
                selectable=True,
                size=MESSAGE_FONT_SIZE,
                color=convert_color(color=color)
            )
        )

    async def add_text(self, text: ft.Text):
        self._message_list_view.controls.append(text)
        await self._message_list_view.update_async()

    def build(self):
        return ft.Row(
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


class MessageSendingBox(CustomControl):
    @di.inject
    def __init__(self, io_manager=IODependencyContainer.io_manager):
        self._io_manager = io_manager
        self._io_manager.input_source = self._handle_input
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
            on_click=self._handle_send_button_click
        )
        self._content = ft.Row(
            controls=[
                self._input_field,
                self._send_button
            ]
        )

        self._value_sent = False

    async def _wait_for_sending(self):
        while not self._value_sent:
            await asyncio.sleep(0.5)

    async def _handle_input(self, prompt: str, color: io.Color):
        self._input_field.hint_text = prompt
        self._input_field.disabled = False
        self._send_button.disabled = False
        self._value_sent = False
        await self._content.update_async()

        await self._wait_for_sending()

        value = self._input_field.value
        self._input_field.value = ''
        self._input_field.hint_text = Messages.MESSAGE
        await self._io_manager.print(value, color=None)
        await self._content.update_async()
        return value

    async def _handle_send_button_click(self, event):
        self._value_sent = True
        self._input_field.disabled = True
        self._send_button.disabled = True
        await self._content.update_async()

    def build(self):
        return self._content
