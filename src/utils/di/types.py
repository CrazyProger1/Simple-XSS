from abc import abstractmethod, ABC


class BaseContainer:
    __dependency_class__: "BaseDependency"

    @classmethod
    @abstractmethod
    def configure(cls): ...

    def __repr__(self):
        return f'<Dependency Container: {self.__class__.__name__}>'


class BaseDependency(ABC):
    @abstractmethod
    def bind(
            self,
            name: str,
            base_type: type,
            default: any,
            container: BaseContainer
    ): ...

    @abstractmethod
    def bind_value(self, value: any): ...

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

    @property
    @abstractmethod
    def nullable(self) -> bool: ...

    def __repr__(self):
        return f'<{self.name}: {self.type.__name__}>'


class BaseContainerMeta(type):
    def __repr__(self):
        return f'<{self.__name__}>'
