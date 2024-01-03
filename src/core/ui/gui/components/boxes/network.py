import flet as ft

from ..control import CustomControl
from ...constants import (
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,

)


class NetworkBox(CustomControl):
    def __init__(self):
        pass

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=None
        )
