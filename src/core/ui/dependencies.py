from src.core import arguments
from src.utils import di
from .factories import UIFactory
from .types import BaseUI, BaseUIFactory


class UIDependencyContainer(di.DeclarativeContainer):
    factory: BaseUIFactory = di.Factory(UIFactory)
    current_ui: BaseUI

    @classmethod
    @di.inject
    def configure(cls, args=arguments.ArgumentsDependencyContainer.current_arguments, factory: BaseUIFactory = factory):
        di.bind(UIDependencyContainer.current_ui, factory.create_ui(args.graphic_mode))


def configure_ui_dependencies():
    UIDependencyContainer.configure()
