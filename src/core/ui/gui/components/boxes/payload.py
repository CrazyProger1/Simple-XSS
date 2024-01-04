import asyncio

import flet as ft

from src.utils import di, packages
from src.core.dependencies import payload_loader
from src.core.ui.dependencies import local_settings
from src.core.services import settings, payloads

from ..control import CustomControl
from ...enums import Messages
from ...constants import (
    TEXT_FONT_SIZE,
    DESCRIPTION_MAX_LINES,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from ...services import banners


class PayloadBox(CustomControl):
    def __init__(self):
        super(PayloadBox, self).__init__()
        self._payload_picker = ft.FilePicker(on_result=self._handle_payload_chosen)
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
            on_click=self._handle_choose_payload_button_click
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
        self._content = ft.Column(
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

    @di.injector.inject
    def _handle_payload_chosen(
            self,
            event: ft.FilePickerResultEvent,
            loader: packages.PackageLoader = payload_loader

    ):
        try:
            payload_cls = payloads.load_payload_class(event.path, loader=loader)
        except (ValueError, ImportError, TypeError):
            text = Messages.PAYLOAD_LOADING_ERROR.format(path=event.path)
            asyncio.create_task(banners.show_warning(text=text))
            return

        self._payload_name_text.value = payload_cls.NAME
        self._payload_description_text.value = payload_cls.DESCRIPTION
        self._payload_author_text.value = f'@{payload_cls.AUTHOR}'
        self._payload_path_field.value = event.path
        asyncio.create_task(self._content.update_async())

    @di.injector.inject
    async def _handle_choose_payload_button_click(self, event, sets: settings.DefaultSettingsScheme = local_settings):
        await self._payload_picker.get_directory_path_async(
            initial_directory=sets.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
