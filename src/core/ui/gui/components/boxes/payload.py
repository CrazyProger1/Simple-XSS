import asyncio

import flet as ft

from src.utils import di
from src.core.dependencies import current_context
from src.core.events import context_changed
from src.core.services import payloads, context

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
            appcontext: context.DefaultContext = current_context
    ):
        path = event.path
        if not path:
            return
        if payloads.is_payload(path):
            appcontext.settings.payload.current = path
            context_changed()

        else:
            asyncio.create_task(
                banners.show_warning(Messages.PAYLOAD_LOADING_ERROR.format(path=path))
            )

    def _update_payload_data(self, path: str):
        if not path or path == self._payload_path_field.value:
            return

        if payloads.is_payload(path):
            payload_cls = payloads.load_payload_class(path)
            self._payload_name_text.value = f'{payload_cls.NAME} - {payload_cls.VERSION or 0.1}'
            self._payload_description_text.value = payload_cls.DESCRIPTION
            self._payload_author_text.value = payload_cls.AUTHOR
            self._payload_path_field.value = path

    @di.injector.inject
    def update_data(self, appcontext: context.DefaultContext = current_context):
        self._content.disabled = appcontext.active.unwrap()
        path = str(appcontext.settings.payload.current)
        self._update_payload_data(path=path)
        asyncio.create_task(self._content.update_async())

    @di.injector.inject
    async def _handle_choose_payload_button_click(self, event, appcontext: context.DefaultContext = current_context):
        await self._payload_picker.get_directory_path_async(
            initial_directory=appcontext.settings.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
