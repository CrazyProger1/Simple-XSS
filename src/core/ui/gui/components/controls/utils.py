import flet as ft

from src.core.ui.gui import GUIEventChannel
from src.utils import io
from .constants import INVALID_TEXT_COLOR, COLOR_TABLE


async def validate_field(field: ft.TextField, *validators):
    if all(validator(field.value) for validator in validators):
        field.color = None
    else:
        field.color = INVALID_TEXT_COLOR

    await field.update_async()


def show_error(message: str):
    GUIEventChannel.internal_error_occurred(error=message)


async def activate():
    await GUIEventChannel.process_activated()


async def deactivate():
    await GUIEventChannel.process_deactivated()


def convert_color(color: io.Color) -> str:
    return COLOR_TABLE.get(color)
