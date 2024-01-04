import flet as ft

from typeguard import typechecked

from src.utils import di
from ...dependencies import main_page, warning_banner, error_banner
from ...constants import WARNING_BANNER_TEXT_COLOR, ERROR_BANNER_TEXT_COLOR


@typechecked
@di.injector.inject
async def show(text: ft.Text, banner: ft.Banner, page: ft.Page = main_page):
    banner.content = text
    page.banner = banner
    page.banner.open = True
    await page.update_async()


@typechecked
@di.injector.inject
async def show_warning(text: str, banner: ft.Banner = warning_banner, page: ft.Page = main_page):
    await show(
        text=ft.Text(text, color=WARNING_BANNER_TEXT_COLOR),
        banner=banner,
        page=page
    )


@typechecked
@di.injector.inject
async def show_error(text: str, banner: ft.Banner = error_banner, page: ft.Page = main_page):
    await show(
        text=ft.Text(text, color=ERROR_BANNER_TEXT_COLOR),
        banner=banner,
        page=page
    )