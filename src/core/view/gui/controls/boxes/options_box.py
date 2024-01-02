import flet as ft

from ..constants import (
    BOX_BORDER_RADIUS,
    BOX_BORDER,
    BOX_PADDING
)
from ..controls import CustomControl


class OptionsBox(CustomControl):
    def build_content(self):
        raise NotImplementedError

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self.build_content()
        )
