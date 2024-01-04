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
        self._hook_picker = ft.FilePicker(on_result=self._handle_hook_chosen)
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
            on_click=self._handle_choose_hook_button_click
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
        self._content = ft.Column(
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

    @di.injector.inject
    def _handle_hook_chosen(
            self,
            event: ft.FilePickerResultEvent,
            loader: packages.PackageLoader = hook_loader,
            sets: settings.DefaultSettingsScheme = local_settings

    ):
        path = event.path
        if not path:
            return
        try:
            hook_cls = hooks.load_hook_class(path, loader=loader)
        except (ValueError, ImportError, TypeError):
            text = Messages.HOOK_LOADING_ERROR.format(path=path)
            asyncio.create_task(banners.show_warning(text=text))
            return

        self._hook_name_text.value = hook_cls.NAME
        self._hook_description_text.value = hook_cls.DESCRIPTION
        self._hook_author_text.value = f'@{hook_cls.AUTHOR}'
        self._hook_path_field.value = path
        sets.hook.current = path
        asyncio.create_task(self._content.update_async())

    @di.injector.inject
    async def _handle_choose_hook_button_click(self, event, sets: settings.DefaultSettingsScheme = local_settings):
        await self._hook_picker.get_directory_path_async(
            initial_directory=sets.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
