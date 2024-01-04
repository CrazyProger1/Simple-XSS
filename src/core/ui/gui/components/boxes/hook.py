import asyncio

import flet as ft

from src.utils import di, packages
from src.core.dependencies import hook_loader
from src.core.ui.dependencies import local_settings
from src.core.services import settings, hooks

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


class HookBox(CustomControl):
    def __init__(self):
        super(HookBox, self).__init__()
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

    @di.injector.inject
    def handle_hook_chosen(
            self,
            event: ft.FilePickerResultEvent,
            loader: packages.PackageLoader = hook_loader

    ):
        try:
            hook_cls = hooks.load_hook_class(event.path, loader=loader)
        except (ValueError, ImportError, TypeError):
            text = Messages.HOOK_LOADING_ERROR.format(path=event.path)
            asyncio.create_task(banners.show_warning(text=text))
            return

        self.hook_name_text.value = hook_cls.NAME
        self.hook_description_text.value = hook_cls.DESCRIPTION
        self.hook_author_text.value = f'@{hook_cls.AUTHOR}'
        self.hook_path_field.value = event.path
        asyncio.create_task(self.content.update_async())

    @di.injector.inject
    async def handle_choose_hook_button_click(self, event, sets: settings.DefaultSettingsScheme = local_settings):
        await self.hook_picker.get_directory_path_async(
            initial_directory=sets.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self.content
        )
