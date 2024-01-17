import flet as ft

from src.utils import di
from src.core.data import (
    DataDependencyContainer,
    Context
)

from src.core.ui.utils import validation
from src.core.hooks import load_hook_class
from .utils import show_error
from .constants import (
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE,
    BOX_BORDER_RADIUS,
    BOX_BORDER,
    BOX_PADDING
)
from ..types import CustomControl
from ...enums import Messages


class HookBox(CustomControl):
    def __init__(self):
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
        self._container = ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=ft.Column(
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
        )

    @di.inject
    async def _handle_choose_hook_button_click(self, _,
                                               context: Context = DataDependencyContainer.context):
        await self._hook_picker.get_directory_path_async(
            initial_directory=context.settings.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    @di.inject
    async def _handle_hook_chosen(self, event: ft.FilePickerResultEvent,
                                  context: Context = DataDependencyContainer.context):
        path = event.path
        if not path:
            return

        if validation.is_valid_hook_path(path=path):
            context.settings.hook.current = path
        else:
            show_error(Messages.HOOK_LOADING_ERROR.format(path=path))

    def _open_hook(self, path: str):
        if not path:
            return
        if path == self._hook_path_field.value:
            return
        try:
            hook = load_hook_class(path)
            self._hook_name_text.value = f'{hook.NAME} - V{hook.VERSION}'
            self._hook_description_text.value = hook.DESCRIPTION
            self._hook_author_text.value = f'@{hook.AUTHOR}'
            self._hook_path_field.value = path
        except (ValueError, ImportError):
            pass

    def update(self, context: Context):
        self._container.disabled = context.process_active.unwrap()
        path = context.settings.hook.current.unwrap()
        self._open_hook(path)

    def validate(self, context: Context) -> bool:
        if not self._hook_path_field.value:
            show_error(Messages.HOOK_REQUIRED)
            return False
        return True

    def build(self):
        return self._container
