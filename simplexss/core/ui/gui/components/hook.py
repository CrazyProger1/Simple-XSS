import flet as ft

from .constants import (
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE,
    BOX_BORDER_RADIUS,
    BOX_BORDER,
    BOX_PADDING
)
from .enums import Messages
from ..types import CustomControl


class HookBox(CustomControl):
    def __init__(self):
        self._hook_picker = ft.FilePicker()
        self.overlay.append(self._hook_picker)

        self._hook_name_text = ft.Text(
            value=Messages.HOOK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._hook_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self._choose_hook_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
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
                            self._hook_path_field,
                            self._choose_hook_button,
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

    def build(self):
        return self._container
