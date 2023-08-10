import importlib.util
import os
from functools import cache


@cache
def import_module(path: str, sep='.'):
    """Imports module from path separated by sep"""

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
    """Imports module from .py file path"""

    try:
        if not os.path.exists(path):
            raise
        *_, filename = os.path.split(path)
        spec = importlib.util.spec_from_file_location(filename.replace('.py', ''), path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module
    except Exception as e:
        raise ImportError(f'Failed to import module: {path}')
