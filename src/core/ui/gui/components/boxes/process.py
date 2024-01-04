import asyncio

import flet as ft
import pyperclip

from src.utils import di
from src.core.events import context_changed
from src.core.dependencies import current_context
from ..control import CustomControl
from ...constants import ICON_SIZE
from ...enums import Messages


class ProcessControlBox(CustomControl):
    def __init__(self):
        super(ProcessControlBox, self).__init__()
        self._run_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            on_click=self._handle_run_button_click,
            tooltip=Messages.RUN
        )
        self._stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self._handle_stop_button_click,
            tooltip=Messages.STOP
        )
        self._copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.BLUE,
            on_click=self._handle_copy_button_click,
            tooltip=Messages.COPY
        )
        self._hook_field = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text=Messages.HOOK
        )

    async def _handle_run_button_click(self, event):
        pass

    async def _handle_stop_button_click(self, event):
        pass

    async def _handle_copy_button_click(self, event):
        pyperclip.copy(self._hook_field.value)

    @di.injector.inject
    def update_data(self, context=current_context):
        self._hook_field.disabled = context.hook is None
        self._hook_field.value = context.hook
        asyncio.create_task(self._hook_field.update_async())

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self._run_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self._stop_button
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self._hook_field
                    ]
                ),
                ft.Column(
                    controls=[
                        self._copy_button
                    ]
                ),
            ]
        )
