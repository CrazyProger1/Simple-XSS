import flet as ft

from src.utils import di

from .components.dependencies import (
    configurate_components_dependencies,
    main_control_dependency
)

main_page_dependency = di.Dependency(ft.Page)


def configurate_gui_dependencies():
    configurate_components_dependencies()
