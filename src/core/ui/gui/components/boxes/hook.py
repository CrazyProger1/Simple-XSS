import asyncio

import flet as ft

from src.utils import di
from src.core.dependencies import current_context
from src.core.services import context, hooks
from src.core.events import context_changed

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
    async def _handle_choose_hook_button_click(self, event, appcontext: context.DefaultContext = current_context):
        await self._hook_picker.get_directory_path_async(
            initial_directory=appcontext.settings.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    @di.injector.inject
    def _handle_hook_chosen(self,
                            event: ft.FilePickerResultEvent,
                            appcontext: context.DefaultContext = current_context):
        path = event.path
        if not path:
            return
        if hooks.is_hook(path):
            appcontext.settings.hook.current = path
            context_changed()

        else:
            asyncio.create_task(
                banners.show_warning(Messages.HOOK_LOADING_ERROR.format(path=path))
            )

    def _update_hook_data(self, path: str):
        if not path or path == self._hook_path_field.value:
            return

        if hooks.is_hook(path):
            hook_cls = hooks.load_hook_class(path)
            self._hook_name_text.value = f'{hook_cls.NAME} - {hook_cls.VERSION or 0.1}'
            self._hook_description_text.value = hook_cls.DESCRIPTION
            self._hook_author_text.value = hook_cls.AUTHOR
            self._hook_path_field.value = path

            asyncio.create_task(
                self._content.update_async()
            )

    @di.injector.inject
    def update_data(self, appcontext: context.DefaultContext = current_context):
        path = appcontext.settings.hook.current
        self._update_hook_data(path=path)

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self._content
        )
