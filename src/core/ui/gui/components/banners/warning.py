import flet as ft

from ...enums import Messages
from ..banner import CustomBanner
from ...constants import (
    WARNING_BANNER_ICON_COLOR,
    WARNING_BANNER_ICON,
    WARNING_BANNER_TEXT_COLOR
)


class WarningBanner(CustomBanner):
    def __init__(self):
        super(WarningBanner, self).__init__(
            bgcolor=ft.colors.AMBER,
            leading=ft.Icon(WARNING_BANNER_ICON, color=WARNING_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, on_click=self.hide, style=ft.ButtonStyle(color=WARNING_BANNER_TEXT_COLOR)),
            ])
