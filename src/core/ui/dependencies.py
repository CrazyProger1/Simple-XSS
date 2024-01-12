from src.utils import di
from src.core import arguments
from .factories import UIFactory
from .base import BaseUI


class UIDependencyContainer(di.DeclarativeContainer):
    current_ui: BaseUI

    @classmethod
    @di.inject
    def configure(cls, args=arguments.ArgumentsDependencyContainer.current_arguments):
        di.bind(UIDependencyContainer.current_ui, UIFactory.create_ui(args.graphic_mode))
