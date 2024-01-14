from src.utils import di, io


class IODependencyContainer(di.DeclarativeContainer):
    io_manager: io.AsyncIOManager = di.Singleton(io.AsyncIOManager)
