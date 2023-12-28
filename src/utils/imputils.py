import importlib.util
import inspect
import os
import sys
from functools import cache


@cache
def import_module(path: str, sep='.'):
    """Imports module from path separated by sep."""

    try:
        components = path.split(sep)
        imported_module = __import__(components[0])
        for comp in components[1:]:
            imported_module = getattr(imported_module, comp)
        return imported_module
    except AttributeError:
        raise ImportError(f'Failed to import module: {path}')


@cache
def import_module_by_filepath(path: str):
    """Imports module by .py file path."""

    directory = os.path.dirname(path)
    sys.path.append(directory)
    try:
        if not os.path.exists(path):
            raise
        *_, filename = os.path.split(path)
        spec = importlib.util.spec_from_file_location(filename.replace('.py', ''), path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module
    except Exception:
        raise ImportError(f'Failed to import module: {path}')
    finally:
        sys.path.remove(directory)


@cache
def import_class_by_filepath(path: str, class_name: str, base_class: type = None) -> type:
    """Imports class from module."""

    module = import_module_by_filepath(path)
    imported_class = getattr(module, class_name, None)
    if not imported_class:
        raise TypeError(f'Class {class_name} not found at {path}')
    if not inspect.isclass(imported_class):
        raise TypeError(f'Not a class {imported_class}')
    if base_class:
        if not issubclass(imported_class, base_class):
            raise TypeError(f'Class must be a subclass of {base_class}')
    return imported_class
