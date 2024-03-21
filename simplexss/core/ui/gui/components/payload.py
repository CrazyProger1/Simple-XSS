import flet as ft

from .constants import (
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE
)
from .enums import Messages
from ..types import CustomControl


class PayloadBox(CustomControl):
    def __init__(self):
        self._payload_picker = ft.FilePicker()
        self.overlay.append(self._payload_picker)

        self._payload_name_text = ft.Text(
            value=Messages.PAYLOAD,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._payload_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self._choose_payload_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
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
                            self._payload_path_field,
                            self._choose_payload_button,
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

    def build(self):
        return self._container
