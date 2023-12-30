import asyncio

import flet as ft

from src.settings.dependencies import current_settings
from src.settings.schemes import DefaultSettingsScheme
from src.utils import di
from .options_box import OptionsBox
from ..constants import TEXT_FONT_SIZE, DESCRIPTION_MAX_LINES
from ..enums import Messages


class PayloadOptionsBox(OptionsBox):
    def __init__(self):
        super(PayloadOptionsBox, self).__init__()
        self.payload_picker = ft.FilePicker(on_result=self.handle_payload_chosen)
        self.overlay.append(self.payload_picker)

        self.payload_name_text = ft.Text(
            value=Messages.PAYLOAD,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self.payload_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self.choose_payload_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.handle_choose_payload_button_click
        )
        self.payload_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self.payload_author_text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            italic=True
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.payload_name_text
                    ]
                ),
                ft.Row(
                    controls=[
                        self.payload_path_field,
                        self.choose_payload_button,
                    ]
                ),
                self.payload_description_text,
                ft.Container(
                    content=self.payload_author_text,
                    alignment=ft.alignment.bottom_right,

                )

            ]
        )

    def handle_payload_chosen(self, event: ft.FilePickerResultEvent):
        self.payload_path_field.value = event.path
        self.payload_name_text.value = 'Some payload'
        self.payload_description_text.value = 'Some payload desc'
        self.payload_author_text.value = '@author'
        asyncio.create_task(self.content.update_async())

    @di.injector.inject
    async def handle_choose_payload_button_click(self, event, settings: DefaultSettingsScheme = current_settings):
        await self.payload_picker.get_directory_path_async(
            initial_directory=settings.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    def build_content(self):
        return self.content
