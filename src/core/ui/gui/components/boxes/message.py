import asyncio

import flet as ft

from src.utils import di, io
from src.core.io.dependencies import io_manager_dependency

from ..control import CustomControl
from ...constants import (
    MESSAGE_SPACING,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    ICON_SIZE, MESSAGE_FONT_SIZE
)

from ...enums import Messages


class MessageAreaBox(CustomControl):
    def __init__(self):
        self._io: io.BaseIOManager = di.injector.get_dependency(io_manager_dependency)
        self._io.print_source = self._handle_print

        self._message_list_view = ft.ListView(
            expand=True,
            spacing=MESSAGE_SPACING,
            auto_scroll=True,
        )

    async def _handle_print(self, *messages, sep: str = ' ', end: str = '\n', color=None):
        text = sep.join(messages)

        self._message_list_view.controls.append(
            ft.Text(text, selectable=True, size=MESSAGE_FONT_SIZE)
        )
        asyncio.create_task(self._message_list_view.update_async())

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


class MessageControlBox(CustomControl):

    def __init__(self):
        self._io = di.injector.get_dependency(io_manager_dependency)
        self._io.input_source = self._handle_input
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

    async def _handle_input(self, prompt, color):
        self._input_field.hint_text = prompt
        self._input_field.disabled = False
        self._send_button.disabled = False
        self._value_sent = False
        await self._content.update_async()

        while not self._value_sent:
            await asyncio.sleep(0.5)

        value = self._input_field.value
        self._input_field.value = ''
        self._input_field.hint_text = Messages.MESSAGE
        await self._content.update_async()
        return value

    async def _handle_send_button_click(self, event):
        self._value_sent = True
        self._input_field.disabled = True
        self._send_button.disabled = True
        await self._content.update_async()

    def build(self):
        return self._content
