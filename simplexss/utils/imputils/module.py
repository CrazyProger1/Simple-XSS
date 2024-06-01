import importlib.util
import logging
import os
import sys
from functools import cache
from types import ModuleType

logger = logging.getLogger("utils.imputils")


@cache
def import_module(path: str) -> ModuleType:
    directory = os.path.dirname(path)
    sys.path.append(directory)
    try:
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
            raise FileNotFoundError(f"Module file not found: {path}")
        *_, filename = os.path.split(path)
        spec = importlib.util.spec_from_file_location(filename.replace(".py", ""), path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)

        logger.debug(f"Module imported: {imported_module}")
        return imported_module
    except Exception as e:
        logger.error(e)
        raise ImportError(f"Failed to import module: {path}")
    finally:
        sys.path.remove(directory)
