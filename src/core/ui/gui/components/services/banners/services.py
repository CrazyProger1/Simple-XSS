import flet as ft

from typeguard import typechecked

from src.utils import di
from src.core.ui.gui.dependencies import main_page_dependency
from ...dependencies import (
    warning_banner_dependency,
    error_banner_dependency
)
from ...constants import (
    WARNING_BANNER_TEXT_COLOR,
    ERROR_BANNER_TEXT_COLOR
)


@typechecked
@di.injector.inject
async def show(text: ft.Text, banner: ft.Banner, page: ft.Page = main_page_dependency):
    banner.content = text
    page.banner = banner
    page.banner.open = True
    await page.update_async()


@typechecked
@di.injector.inject
async def show_warning(text: str, banner: ft.Banner = warning_banner_dependency, page: ft.Page = main_page_dependency):
    await show(
        text=ft.Text(text, color=WARNING_BANNER_TEXT_COLOR),
        banner=banner,
        page=page
    )


@typechecked
@di.injector.inject
async def show_error(text: str, banner: ft.Banner = error_banner_dependency, page: ft.Page = main_page_dependency):
    await show(
        text=ft.Text(text, color=ERROR_BANNER_TEXT_COLOR),
        banner=banner,
        page=page
    )
