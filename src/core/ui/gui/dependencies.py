import flet as ft

from src.utils import di
from .components import BaseComponentManager, ComponentManager


class GUIDependencyContainer(di.DeclarativeContainer):
    main_page: ft.Page
    component_manager: BaseComponentManager = di.Singleton(ComponentManager)


def configure_gui_dependencies():
    GUIDependencyContainer.configure()
