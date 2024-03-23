import inspect

from .module import import_module
from .logging import logger


def import_class(path: str, class_name: str, base: type = object):
    module = import_module(path)
    imported_class = getattr(module, class_name, None)
    if not imported_class:
        logger.error(f'Class {class_name} not found at {path}')
        raise ImportError(f'Class {class_name} not found at {path}')
    if not inspect.isclass(imported_class):
        logger.error(f'Not a class {imported_class}')
        raise TypeError(f'Not a class {imported_class}')

    if not issubclass(imported_class, base):
        logger.error(f'Class must be a subclass of {base}')
        raise TypeError(f'Class must be a subclass of {base}')

    logger.debug(f'Class imported: {imported_class}')
    return imported_class
