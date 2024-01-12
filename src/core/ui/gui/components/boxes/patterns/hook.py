import asyncio

import flet as ft

from src.utils import di
from src.core import hooks
from src.core.context.dependencies import current_context_dependency
from src.core.ui.utils import validation

from ..base import CustomControl
from ..enums import Messages
from ..constants import (
    TEXT_FONT_SIZE,
    DESCRIPTION_MAX_LINES,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from ..services import banners


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
    async def _handle_choose_hook_button_click(self, event, context=current_context_dependency):
        await self._hook_picker.get_directory_path_async(
            initial_directory=context.settings.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    @di.injector.inject
    def _handle_hook_chosen(
            self,
            event: ft.FilePickerResultEvent,
            context=current_context_dependency):
        path = event.path
        if path and validation.is_valid_hook_path(path=path):
            context.settings.hook.current = path

        else:
            asyncio.create_task(
                banners.show_warning(Messages.HOOK_LOADING_ERROR.format(path=path))
            )

    def _update_hook_data(self, context):
        path = str(context.settings.hook.current)
        if path and validation.is_valid_hook_path(path=path):
            hook_cls = hooks.load_hook_class(path)
            self._hook_name_text.value = f'{hook_cls.NAME} - {hook_cls.VERSION or 0.1}'
            self._hook_description_text.value = hook_cls.DESCRIPTION
            self._hook_author_text.value = f'@{hook_cls.AUTHOR}'
            self._hook_path_field.value = path

    def update_data(self, context):
        self._content.disabled = context.process_active.unwrap()
        self._update_hook_data(context=context)

    def setup_data(self, context):
        self._content.disabled = context.process_active.unwrap()
        self._update_hook_data(context=context)

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
