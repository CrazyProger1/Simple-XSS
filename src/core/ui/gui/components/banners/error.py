import flet as ft

from ...enums import Messages

from ...constants import (
    ERROR_BANNER_ICON,
    ERROR_BANNER_ICON_COLOR,
    ERROR_BANNER_TEXT_COLOR
)


class ErrorBanner(ft.Banner):
    def __init__(self):
        super(ErrorBanner, self).__init__(
            bgcolor=ft.colors.AMBER,
            leading=ft.Icon(ERROR_BANNER_ICON, color=ERROR_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, on_click=self.hide, style=ft.ButtonStyle(color=ERROR_BANNER_TEXT_COLOR)),
            ])
