import flet as ft

from src.core.payloads import load_payload_class
from src.core.ui.utils import validation
from src.utils import di

from .constants import (
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    DESCRIPTION_MAX_LINES,
    TEXT_FONT_SIZE
)
from src.core.context import (
    DefaultContext,
    ContextDependenciesContainer
)
from .utils import show_error
from ..types import CustomControl
from ...enums import Messages


class PayloadBox(CustomControl):
    def __init__(self):
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

        self._container = ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=ft.Column(
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

        )

    @di.inject
    async def _handle_choose_payload_button_click(
            self, _,
            context: DefaultContext = ContextDependenciesContainer.current_context
    ):
        await self._payload_picker.get_directory_path_async(
            initial_directory=context.settings.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    @di.inject
    async def _handle_payload_chosen(self, event: ft.FilePickerResultEvent,
                                     context: DefaultContext = ContextDependenciesContainer.current_context):
        path = event.path
        if not path:
            return

        if validation.is_valid_payload_path(path=path):
            context.settings.payload.current = path
        else:
            show_error(Messages.PAYLOAD_LOADING_ERROR.format(path=path))

    def _open_payload(self, path: str):
        if not path:
            return
        if path == self._payload_path_field.value:
            return
        try:
            hook = load_payload_class(path)
            self._payload_name_text.value = f'{hook.NAME} - V{hook.VERSION}'
            self._payload_description_text.value = hook.DESCRIPTION
            self._payload_author_text.value = f'@{hook.AUTHOR}'
            self._payload_path_field.value = path
        except (ValueError, ImportError):
            pass

    def update(self, context: DefaultContext):
        self._container.disabled = context.process_active.unwrap()
        path = context.settings.payload.current.unwrap()
        self._open_payload(path)

    def validate(self, context: DefaultContext) -> bool:
        if not self._payload_path_field.value:
            show_error(Messages.PAYLOAD_REQUIRED)
            return False
        return True

    def build(self):
        return self._container
