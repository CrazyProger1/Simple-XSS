import asyncio

import flet as ft

from src.utils import di
from src.core import payloads
from src.core.context.dependencies import current_context_dependency
from src.core.context.events import context_changed
from src.core.ui.utils import validation
from ..base import CustomControl
from ..constants import (
    TEXT_FONT_SIZE,
    DESCRIPTION_MAX_LINES,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from ..enums import Messages
from ..services import banners


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
    async def _handle_choose_payload_button_click(self, event, appcontext=current_context_dependency):
        await self._payload_picker.get_directory_path_async(
            initial_directory=appcontext.settings.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    @di.injector.inject
    def _handle_payload_chosen(
            self,
            event: ft.FilePickerResultEvent,
            context=current_context_dependency
    ):
        path = event.path
        if path and validation.is_valid_payload_path(path=path):
            context.settings.payload.current = path
            context_changed()

        else:
            asyncio.create_task(
                banners.show_warning(Messages.PAYLOAD_LOADING_ERROR.format(path=path))
            )

    def _update_payload_data(self, context):
        path = str(context.settings.payload.current)
        if path and validation.is_valid_payload_path(path=path):
            payload_cls = payloads.load_payload_class(path)
            self._payload_name_text.value = f'{payload_cls.NAME} - {payload_cls.VERSION or 0.1}'
            self._payload_description_text.value = payload_cls.DESCRIPTION
            self._payload_author_text.value = f'@{payload_cls.AUTHOR}'
            self._payload_path_field.value = path

    def update_data(self, context):
        self._content.disabled = context.process_active.unwrap()
        self._update_payload_data(context=context)

    def setup_data(self, context):
        self._content.disabled = context.process_active.unwrap()
        self._update_payload_data(context=context)

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
