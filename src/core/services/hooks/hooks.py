from src.utils import packages
from src.core.enums import Protocol


class BaseHook(packages.BasePackage):
    TRANSPORT: Protocol
