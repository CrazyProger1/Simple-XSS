from abc import abstractmethod, ABC


class BaseContainer:

    @classmethod
    @abstractmethod
    def configure(cls): ...


class BaseDependency(ABC):
    @abstractmethod
    def bind(self, value: any): ...

    @property
    @abstractmethod
    def container(self) -> BaseContainer: ...

    @property
    @abstractmethod
    def type(self) -> type: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def value(self) -> any: ...

    def __repr__(self):
        return f'<{self.name}: {self.type.__name__}>'


class BaseContainerMeta(type):
    def __repr__(self):
        return f'<{self.__name__}>'
