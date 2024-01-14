import flet as ft
import pyperclip

from src.core.context import DefaultContext
from .constants import ICON_SIZE
from .utils import activate, deactivate
from ..types import CustomControl
from ...enums import Messages


class ProcessBox(CustomControl):
    def __init__(self):
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

    async def _handle_activate_button_click(self, _):
        await activate()

    async def _handle_deactivate_button_click(self, _):
        await deactivate()

    async def _handle_copy_button_click(self, _):
        pyperclip.copy(self._hook_field.value)

    def setup(self, context: DefaultContext):
        self._copy_button.disabled = True

    def update(self, context: DefaultContext):
        process_active = context.process_active.unwrap()
        self._copy_button.disabled = not process_active
        self._activate_button.disabled = process_active
        self._deactivate_button.disabled = not process_active

    def build(self):
        return ft.Row(
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
