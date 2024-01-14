from src.utils import di
from .process import BaseProcess, Process


class LogicDependenciesContainer(di.DeclarativeContainer):
    process: BaseProcess = di.Singleton(Process)


def configure_logic_dependencies():
    LogicDependenciesContainer.configure()
