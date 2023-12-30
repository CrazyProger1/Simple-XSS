import asyncio

import flet as ft

from src.settings.dependencies import current_settings
from src.settings.schemes import DefaultSettingsScheme
from src.utils import di
from .options_box import OptionsBox
from ..constants import TEXT_FONT_SIZE, DESCRIPTION_MAX_LINES
from ..enums import Messages


class HookOptionsBox(OptionsBox):
    def __init__(self):
        super(HookOptionsBox, self).__init__()
        self.hook_picker = ft.FilePicker(on_result=self.handle_hook_chosen)
        self.overlay.append(self.hook_picker)

        self.hook_name_text = ft.Text(
            value=Messages.HOOK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self.hook_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self.choose_hook_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.handle_choose_hook_button_click
        )
        self.hook_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self.hook_author_text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            italic=True
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.hook_name_text
                    ]
                ),
                ft.Row(
                    controls=[
                        self.hook_path_field,
                        self.choose_hook_button,
                    ]
                ),
                self.hook_description_text,
                ft.Container(
                    content=self.hook_author_text,
                    alignment=ft.alignment.bottom_right,

                )

            ]
        )

    def handle_hook_chosen(self, event: ft.FilePickerResultEvent):
        self.hook_path_field.value = event.path
        self.hook_name_text.value = 'Some hook'
        self.hook_description_text.value = 'Some hook desc'
        self.hook_author_text.value = '@author'
        asyncio.create_task(self.content.update_async())

    @di.injector.inject
    async def handle_choose_hook_button_click(self, event, settings: DefaultSettingsScheme = current_settings):
        await self.hook_picker.get_directory_path_async(
            initial_directory=settings.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    def build_content(self):
        return self.content
