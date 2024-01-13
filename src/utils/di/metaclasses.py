from .dependencies import Dependency
from .types import BaseContainerMeta, BaseDependency


class DeclarativeContainerMeta(BaseContainerMeta):
    def __new__(mcs, clsname, superclasses, attributedict):
        annotations: dict = attributedict.get('__annotations__')
        dependency_class = attributedict.get('__dependency_class__', Dependency)
        cls = super().__new__(mcs, clsname, superclasses, attributedict)
        if annotations:
            for name, tp in annotations.items():
                default = attributedict.get(name)
                kwargs_to_bound = {
                    'name': name,
                    'base_type': tp,
                    'container': cls,
                    'default': None
                }
                if isinstance(default, BaseDependency):
                    dependency = default

                else:
                    dependency = dependency_class()
                    kwargs_to_bound.update({'default': default})

                dependency.bind(
                    **kwargs_to_bound
                )

                setattr(cls, name, dependency)
        return cls
