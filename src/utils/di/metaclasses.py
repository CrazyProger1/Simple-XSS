from .dependencies import Dependency
from .types import BaseContainerMeta


class DeclarativeContainerMeta(BaseContainerMeta):
    def __new__(mcs, clsname, superclasses, attributedict):
        annotations: dict = attributedict.get('__annotations__')
        cls = super().__new__(mcs, clsname, superclasses, attributedict)
        if annotations:
            for name, tp in annotations.items():
                default = attributedict.get(name)
                dependency = Dependency(
                    name=name,
                    base_type=tp,
                    container=cls,
                    default=default
                )
                setattr(cls, name, dependency)
        return cls
