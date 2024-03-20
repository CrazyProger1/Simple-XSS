import importlib.util
import os
import sys
from functools import cache
from types import ModuleType


@cache
def import_module(path: str) -> ModuleType:
    directory = os.path.dirname(path)
    sys.path.append(directory)
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Module file not found: {path}")
        *_, filename = os.path.split(path)
        spec = importlib.util.spec_from_file_location(filename.replace('.py', ''), path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module
    except Exception:
        raise ImportError(f'Failed to import module: {path}')
    finally:
        sys.path.remove(directory)
