import asyncio

import flet as ft
import pyperclip

from src.utils import di
from src.core.context.dependencies import current_context_dependency
from src.core.ui.events import (
    ui_process_activated,
    ui_process_deactivated
)

from ..control import CustomControl
from ...constants import ICON_SIZE
from ...enums import Messages


class ProcessControlBox(CustomControl):
    def __init__(self):
        super(ProcessControlBox, self).__init__()
        self._activate_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            on_click=self._handle_activate_button_click,
            tooltip=Messages.RUN
        )
        self._deactivate_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self._handle_deactivate_button_click,
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
        self._content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self._activate_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self._deactivate_button
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

    async def _handle_activate_button_click(self, event):
        await ui_process_activated()

    async def _handle_deactivate_button_click(self, event):
        await ui_process_deactivated()

    async def _handle_copy_button_click(self, event):
        pyperclip.copy(self._hook_field.value)

    @di.injector.inject
    def update_data(self, context=current_context_dependency):
        hook_code = context.hook_code.unwrap()
        process_active = context.process_active.unwrap()
        self._deactivate_button.disabled = not process_active
        self._activate_button.disabled = process_active

        self._hook_field.disabled = not process_active

        if process_active:
            self._hook_field.value = hook_code
        else:
            self._hook_field.value = ''

        asyncio.create_task(self._content.update_async())

    def build(self):
        return self._content
